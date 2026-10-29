
import json
import logging
import re
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path

import obsws_python as obs
from playwright.sync_api import sync_playwright

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.json"
LOG_FILE = BASE_DIR / "automation.log"
PROFILE_DIR = BASE_DIR / "profil_google_meet"

START_DATE = date(2026, 10, 29)
END_DATE = date(2026, 10, 29)
POLL_SECONDS = 15

_playwright = None
_browser_context = None
_meet_page = None


# ============================================================
# JOURNAL
# ============================================================

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )


# ============================================================
# CONFIG.JSON
# ============================================================

def load_config():
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Fichier introuvable : {CONFIG_FILE}")

    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        config = json.load(file)

    for key in ("host", "port", "password", "sessions"):
        if key not in config:
            raise ValueError(f"Clé manquante dans config.json : {key}")

    for session in config["sessions"]:
        for key in ("name", "days", "start", "end", "meet_url"):
            if key not in session:
                raise ValueError(
                    f"Clé '{key}' manquante dans une session."
                )

    return config


# ============================================================
# NOM DES FICHIERS
# ============================================================

def safe_filename(value):
    value = str(value).strip()
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", value)
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value.strip(" .-")


def build_recording_name(session_name, start_datetime):
    return (
        f"{start_datetime:%Y-%m-%d}_"
        f"{safe_filename(session_name)}_"
        f"{start_datetime:%H-%M}"
    )


# ============================================================
# OBS STUDIO
# ============================================================

def connect_obs(config):
    client = obs.ReqClient(
        host=config["host"],
        port=int(config["port"]),
        password=config["password"],
        timeout=5,
    )
    status = client.get_record_status()
    logging.info(
        "Connexion OBS réussie. Enregistrement actif : %s",
        status.output_active,
    )
    return client


def obs_is_recording(client):
    return bool(client.get_record_status().output_active)


def set_obs_filename(client, filename):
    """
    Configure le nom de fichier via OBS WebSocket.
    Le dossier de sortie reste celui défini dans OBS.
    """
    if not hasattr(client, "set_profile_parameter"):
        raise RuntimeError(
            "set_profile_parameter indisponible. "
            "Mets à jour obsws-python."
        )

    client.set_profile_parameter(
        "Output",
        "FilenameFormatting",
        filename,
    )


def start_recording(client, session_name, start_datetime):
    if obs_is_recording(client):
        logging.error("OBS enregistre déjà : aucun nouvel enregistrement.")
        return False

    filename = build_recording_name(session_name, start_datetime)

    try:
        set_obs_filename(client, filename)
        logging.info("Nom de fichier demandé à OBS : %s", filename)

        client.start_record()
        time.sleep(2)

        if not obs_is_recording(client):
            logging.error("OBS n'a pas confirmé le démarrage.")
            return False

        logging.info("Enregistrement démarré : %s", filename)
        return True

    except Exception:
        logging.exception("Échec du démarrage de l'enregistrement OBS.")
        return False


def stop_recording(client, session_name):
    try:
        if obs_is_recording(client):
            client.stop_record()
            time.sleep(2)
            logging.info("Enregistrement arrêté : %s", session_name)
    except Exception:
        logging.exception("Erreur pendant l'arrêt OBS.")

def leave_google_meet(page):
    """Quitte la réunion Google Meet."""
    patterns = [
        r"quitter l'appel",
        r"quitter la réunion",
        r"leave call",
        r"leave meeting",
    ]

    for pattern in patterns:
        try:
            button = page.get_by_role(
                "button",
                name=re.compile(pattern, re.IGNORECASE),
            ).first

            if button.is_visible(timeout=1000):
                button.click(timeout=3000)
                logging.info("Réunion Google Meet quittée.")
                return True
        except Exception:
            continue

    logging.warning("Bouton pour quitter Google Meet introuvable.")
    return False
# ============================================================
# PLAYWRIGHT / GOOGLE MEET
# ============================================================

def init_browser():
    global _playwright, _browser_context, _meet_page

    if _browser_context is not None:
        return _meet_page

    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    _playwright = sync_playwright().start()

    _browser_context = _playwright.chromium.launch_persistent_context(
        user_data_dir=str(PROFILE_DIR),
        headless=False,
        args=["--start-maximized"],
        viewport=None,
    )

    if _browser_context.pages:
        _meet_page = _browser_context.pages[0]
    else:
        _meet_page = _browser_context.new_page()

    return _meet_page


def close_browser():
    global _playwright, _browser_context, _meet_page

    try:
        if _browser_context is not None:
            _browser_context.close()
    except Exception:
        logging.exception("Erreur à la fermeture du navigateur.")

    try:
        if _playwright is not None:
            _playwright.stop()
    except Exception:
        logging.exception("Erreur à l'arrêt de Playwright.")

    _playwright = None
    _browser_context = None
    _meet_page = None


def click_button_by_name(page, patterns, timeout=1200):
    for pattern in patterns:
        try:
            button = page.get_by_role(
                "button",
                name=re.compile(pattern, re.IGNORECASE),
            ).first

            if button.is_visible(timeout=timeout):
                button.click(timeout=timeout)
                logging.info("Bouton cliqué : %s", pattern)
                return True
        except Exception:
            continue

    return False


def close_camera_microphone_popup(page):
    """
    Ferme la fenêtre de présentation caméra/micro en cliquant
    sur sa croix accessible, si elle est présente.
    """
    selectors = [
        'button[aria-label="Fermer"]',
        'button[aria-label="Close"]',
        '[role="button"][aria-label="Fermer"]',
        '[role="button"][aria-label="Close"]',
        'button[title="Fermer"]',
        'button[title="Close"]',
    ]

    for _ in range(5):
        for selector in selectors:
            try:
                button = page.locator(selector).first

                if button.is_visible(timeout=500):
                    button.click(timeout=1500)
                    page.wait_for_timeout(1000)
                    logging.info(
                        "Fenêtre caméra/micro fermée avec la croix."
                    )
                    return True
            except Exception:
                pass

        page.wait_for_timeout(500)

    logging.info(
        "Croix de la fenêtre caméra/micro non détectée "
        "ou fenêtre absente."
    )
    return False


def continue_without_microphone_camera(page):
    patterns = [
        r"continuer sans micro ni caméra",
        r"continuer sans micro",
        r"continue without microphone and camera",
        r"continue without mic",
    ]

    for _ in range(5):
        if click_button_by_name(page, patterns):
            page.wait_for_timeout(1000)
            return True
        page.wait_for_timeout(500)

    return False


def disable_microphone_and_camera(page):
    microphone_patterns = [
        r"^désactiver le micro$",
        r"^couper le micro$",
        r"^turn off microphone$",
        r"^turn off mic$",
    ]

    camera_patterns = [
        r"^désactiver la caméra$",
        r"^couper la caméra$",
        r"^turn off camera$",
    ]

    click_button_by_name(page, microphone_patterns, timeout=700)
    click_button_by_name(page, camera_patterns, timeout=700)


def meeting_is_joined(page):
    patterns = [
        r"quitter l'appel",
        r"quitter la réunion",
        r"leave call",
        r"leave meeting",
    ]

    for pattern in patterns:
        try:
            button = page.get_by_role(
                "button",
                name=re.compile(pattern, re.IGNORECASE),
            ).first

            if button.is_visible(timeout=700):
                return True
        except Exception:
            pass

    return False


def join_meet(url):
    page = init_browser()

    logging.info("Ouverture de Google Meet : %s", url)
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)

    # Fermer la fenêtre de présentation si elle apparaît.
    close_camera_microphone_popup(page)

    # Si Meet propose un bouton pour continuer sans périphériques,
    # le choisir plutôt que d'activer le micro ou la caméra.
    continue_without_microphone_camera(page)
    disable_microphone_and_camera(page)

    join_patterns = [
        r"participer à la réunion",
        r"participer maintenant",
        r"join now",
    ]

    click_button_by_name(page, join_patterns, timeout=2000)

    for _ in range(30):
        if meeting_is_joined(page):
            logging.info("Participation à Google Meet confirmée.")
            return True

        try:
            request_button = page.get_by_role(
                "button",
                name=re.compile(
                    r"demander à participer|ask to join",
                    re.IGNORECASE,
                ),
            ).first

            if request_button.is_visible(timeout=300):
                logging.warning(
                    "En attente de l'autorisation de l'organisateur."
                )
                return False
        except Exception:
            pass

        # Certaines interfaces affichent le bouton avec un léger délai.
        click_button_by_name(page, join_patterns, timeout=500)
        page.wait_for_timeout(1000)

    logging.error(
        "Participation non confirmée. Aucun enregistrement démarré."
    )
    return False


# ============================================================
# EMPLOI DU TEMPS
# ============================================================

def parse_clock(value):
    return datetime.strptime(value, "%H:%M").time()


def session_for_datetime(config, current):
    current_day = current.weekday()
    current_time = current.time().replace(tzinfo=None)

    for session in config["sessions"]:
        if current_day not in session["days"]:
            continue

        start = parse_clock(session["start"])
        end = parse_clock(session["end"])

        if start <= current_time < end:
            return session

    return None


def session_start_datetime(session, day):
    return datetime.combine(day, parse_clock(session["start"]))


# ============================================================
# MODE PROGRAMMÉ
# ============================================================

def run_scheduler(config):
    client = connect_obs(config)

    active_session = None
    active_start = None
    recording_started = False
    attempted_slots = set()

    logging.info(
        "Automatisation active du %s au %s inclus.",
        START_DATE,
        END_DATE,
    )
    logging.info("Fuseau horaire : celui de Windows.")
    logging.info("En attente des créneaux de cours...")

    try:
        while True:
            now = datetime.now()

            if now.date() > END_DATE:
                logging.info("Période terminée.")
                break

            if now.date() < START_DATE:
                time.sleep(POLL_SECONDS)
                continue

            session = session_for_datetime(config, now)

            if session is None:
                if recording_started and active_session is not None:
                    # 1. Arrêter l'enregistrement OBS
                    stop_recording(client, active_session["name"])
                    recording_started = False

                    # 2. Quitter Google Meet
                    if _meet_page is not None:
                        leave_google_meet(_meet_page)

                    
                    # 3. Réinitialiser la session active
                    active_session = None
                    active_start = None

                time.sleep(POLL_SECONDS)
                continue

            scheduled_start = session_start_datetime(session, now.date())
            slot_key = (
                session["name"],
                scheduled_start.isoformat(),
                session["meet_url"],
            )

            if slot_key in attempted_slots:
                time.sleep(POLL_SECONDS)
                continue

            # Empêche de tenter le même créneau plusieurs fois
            # si Meet ou OBS refuse de démarrer.
            attempted_slots.add(slot_key)

            if recording_started and active_session is not None:
                stop_recording(client, active_session["name"])
                recording_started = False

            active_session = None
            active_start = None

            logging.info(
                "Créneau : %s (%s–%s).",
                session["name"],
                session["start"],
                session["end"],
            )

            try:
                joined = join_meet(session["meet_url"])
            except Exception:
                logging.exception("Erreur de connexion à Google Meet.")
                joined = False

            if joined:
                recording_started = start_recording(
                    client,
                    session["name"],
                    scheduled_start,
                )

                if recording_started:
                    active_session = session
                    active_start = scheduled_start
            else:
                logging.error(
                    "Cours non enregistré : participation non confirmée."
                )

            time.sleep(POLL_SECONDS)

    except KeyboardInterrupt:
        logging.info("Arrêt manuel demandé.")

    finally:
        if recording_started and active_session is not None:
            # Arrêter OBS avant de quitter Meet
            stop_recording(client, active_session["name"])
            recording_started = False

        # Quitter Google Meet si l'onglet existe encore
        if _meet_page is not None:
            leave_google_meet(_meet_page)

        # Fermer le navigateur
        close_browser()


# ============================================================
# MODE TEST IMMÉDIAT
# ============================================================

def test_now(config):
    if not config["sessions"]:
        logging.error("Aucune session configurée.")
        return

    client = connect_obs(config)

    if obs_is_recording(client):
        logging.error(
            "OBS enregistre déjà. Arrête cet enregistrement avant le test."
        )
        return

    session = config["sessions"][0]
    now = datetime.now().replace(second=0, microsecond=0)
    recording_started = False

    try:
        logging.info(
            "Mode test immédiat : %s. Vérifie que le lien Meet "
            "correspond bien au cours actuel.",
            session["name"],
        )

        if not join_meet(session["meet_url"]):
            logging.error(
                "Participation non confirmée. "
                "Aucun enregistrement lancé."
            )
            return

        recording_started = start_recording(
            client,
            session["name"] + "-TEST",
            now,
        )

        if not recording_started:
            return

        logging.info(
            "Test en cours. Appuie sur Ctrl+C pour arrêter."
        )

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logging.info("Arrêt du test demandé.")

    finally:
        if recording_started:
            stop_recording(client, session["name"] + "-TEST")

        if _meet_page is not None:
            leave_google_meet(_meet_page)

        close_browser()


# ============================================================
# DÉMARRAGE
# ============================================================

def main():
    setup_logging()

    try:
        config = load_config()

        if "--test-now" in sys.argv:
            test_now(config)
        else:
            run_scheduler(config)

    except Exception:
        logging.exception("Erreur fatale de l'automatisation.")
        close_browser()


if __name__ == "__main__":
    main()
