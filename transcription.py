
from pathlib import Path
from datetime import timedelta
import argparse
import logging
import re
import time

from faster_whisper import WhisperModel


# ============================================================
# CONFIGURATION
# ============================================================

RECORDINGS_DIR = Path(r"C:\Users\ibrah\Desktop\Cours-Rec")
TRANSCRIPTIONS_DIR = RECORDINGS_DIR / "transcriptions"

# Modèle adapté pour commencer sur un PC sans GPU puissant.
MODEL_SIZE = "base"
LANGUAGE = "fr"

# Extensions de fichiers vidéo/audio prises en charge.
MEDIA_EXTENSIONS = {
    ".mp4", ".mkv", ".mov", ".avi", ".webm",
    ".mp3", ".wav", ".m4a", ".aac", ".flac", ".wma"
}

POLL_SECONDS = 20
STABLE_CHECKS = 3
STABLE_INTERVAL = 5

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)


# ============================================================
# VERIFICATION DU FICHIER
# ============================================================

def wait_until_file_is_stable(path: Path) -> bool:
    """Attend que la taille du fichier cesse de changer."""
    previous_size = -1
    stable_count = 0

    for _ in range(60):
        try:
            current_size = path.stat().st_size
        except (FileNotFoundError, PermissionError):
            return False

        if current_size > 0 and current_size == previous_size:
            stable_count += 1
        else:
            stable_count = 0

        if stable_count >= STABLE_CHECKS:
            return True

        previous_size = current_size
        time.sleep(STABLE_INTERVAL)

    logging.warning("Le fichier semble toujours en cours d'écriture : %s", path.name)
    return False


def format_timestamp(seconds: float) -> str:
    """Convertit une durée en HH:MM:SS."""
    return str(timedelta(seconds=max(0, int(seconds))))


def clean_text(text: str) -> str:
    """Nettoie les espaces superflus."""
    return re.sub(r"\s+", " ", text).strip()


# ============================================================
# TRANSCRIPTION
# ============================================================

def transcribe_file(model: WhisperModel, media_path: Path) -> bool:
    """Transcrit un enregistrement et produit un fichier TXT."""
    output_path = TRANSCRIPTIONS_DIR / f"{media_path.stem}.txt"

    if output_path.exists():
        logging.info("Transcription déjà présente : %s", output_path.name)
        return True

    logging.info("Début de la transcription : %s", media_path.name)

    try:
        segments, info = model.transcribe(
            str(media_path),
            language=LANGUAGE,
            task="transcribe",
            beam_size=3,
            vad_filter=True,
            condition_on_previous_text=True,
        )

        TRANSCRIPTIONS_DIR.mkdir(parents=True, exist_ok=True)

        segment_count = 0

        with output_path.open("w", encoding="utf-8") as output:
            output.write(f"TRANSCRIPTION DU COURS\n")
            output.write(f"Fichier source : {media_path.name}\n")
            output.write(f"Langue détectée : {info.language}\n")
            output.write(
                f"Durée approximative : {format_timestamp(info.duration)}\n"
            )
            output.write("=" * 60 + "\n\n")

            for segment in segments:
                text = clean_text(segment.text)

                if not text:
                    continue

                start = format_timestamp(segment.start)
                end = format_timestamp(segment.end)

                output.write(f"[{start} - {end}] {text}\n\n")
                output.flush()
                segment_count += 1

        if segment_count == 0:
            output_path.unlink(missing_ok=True)
            logging.warning(
                "Aucune parole détectée dans %s. Vérifie le son.",
                media_path.name,
            )
            return False

        logging.info(
            "Transcription terminée : %s (%s segments)",
            output_path,
            segment_count,
        )
        return True

    except Exception:
        logging.exception("Erreur de transcription pour %s", media_path.name)
        return False


# ============================================================
# SCAN ET SURVEILLANCE
# ============================================================

def find_media_files():
    """Liste les enregistrements dans le dossier configuré."""
    if not RECORDINGS_DIR.exists():
        logging.error("Dossier introuvable : %s", RECORDINGS_DIR)
        return []

    return sorted(
        path
        for path in RECORDINGS_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in MEDIA_EXTENSIONS
    )


def process_pending_files(model: WhisperModel) -> int:
    """Transcrit les fichiers qui n'ont pas encore de TXT."""
    files = find_media_files()
    processed = 0

    for media_path in files:
        output_path = TRANSCRIPTIONS_DIR / f"{media_path.stem}.txt"

        if output_path.exists():
            continue

        logging.info("Nouvel enregistrement détecté : %s", media_path.name)

        if not wait_until_file_is_stable(media_path):
            continue

        if transcribe_file(model, media_path):
            processed += 1

    return processed


def main():
    parser = argparse.ArgumentParser(
        description="Transcription locale des cours enregistrés avec OBS."
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Effectue un seul scan puis quitte.",
    )
    args = parser.parse_args()

    TRANSCRIPTIONS_DIR.mkdir(parents=True, exist_ok=True)

    logging.info("Dossier des enregistrements : %s", RECORDINGS_DIR)
    logging.info("Dossier des transcriptions : %s", TRANSCRIPTIONS_DIR)
    logging.info("Chargement du modèle Whisper '%s'...", MODEL_SIZE)

    try:
        model = WhisperModel(
            MODEL_SIZE,
            device="cpu",
            compute_type="int8",
        )
    except Exception:
        logging.exception(
            "Impossible de charger Whisper. Vérifie Internet au premier lancement "
            "et l'espace disque disponible."
        )
        return

    logging.info("Whisper est prêt.")

    if args.once:
        process_pending_files(model)
        logging.info("Scan terminé.")
        return

    logging.info("Surveillance active. Appuie sur Ctrl+C pour arrêter.")

    try:
        while True:
            process_pending_files(model)
            time.sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        logging.info("Surveillance arrêtée par l'utilisateur.")


if __name__ == "__main__":
    main()
