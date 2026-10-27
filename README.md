
# Rec Cours Automation

Automatisation locale de Google Meet et OBS Studio pour faciliter l'enregistrement de cours, avec un emploi du temps personnalisable.

## Fonctionnalités

- Emploi du temps par jour et par créneau.
- Ouverture de Google Meet avec Playwright.
- Tentative de fermeture de la fenêtre d'introduction de Meet.
- Contrôle de l'enregistrement par OBS WebSocket.
- Nommage des enregistrements et journalisation.
- Configuration individuelle pour chaque utilisateur.

## Prérequis

- Windows 10 ou 11
- Python 3.10+
- OBS Studio
- Google Meet accessible avec votre propre compte
- Autorisation d'enregistrer les cours

## Installation

Ouvrez PowerShell dans le dossier du projet :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install chromium
Copy-Item config.example.json config.json
notepad .\config.json
```

Renseignez votre mot de passe OBS local, vos liens Meet, vos dates et vos horaires dans `config.json`.

Dans OBS, activez le serveur WebSocket, vérifiez son port et son mot de passe, et configurez correctement les sources vidéo et audio.

Au premier lancement, connectez-vous manuellement à Google dans la fenêtre Chromium ouverte par le programme.

## Tester

```powershell
python -m py_compile .\automation.py
python .\automation.py --test-now
```

Le test utilise le lien de la première session. Vérifiez-le avant de démarrer. Arrêtez avec `Ctrl+C` et vérifiez le fichier créé.

## Lancer l'emploi du temps

```powershell
python .\automation.py
```

L'ordinateur, OBS et le programme doivent rester actifs pendant les créneaux prévus.

## Sécurité

- Ne publiez jamais `config.json`.
- Ne partagez jamais `profil_google_meet/`.
- Ne publiez ni cookies, ni mots de passe, ni vidéos de cours.
- N'essayez pas de contourner une salle d'attente ou une autorisation de participation.
- Obtenez l'accord nécessaire avant d'enregistrer.

## Limites

Les éléments de l'interface Google Meet peuvent changer. Le bouton de fermeture et les boutons de participation ne sont pas garantis sur toutes les versions. Testez le fonctionnement sur votre ordinateur avant toute utilisation réelle.

Le format du nom de fichier dépend aussi de la version d'OBS WebSocket et de sa configuration. Vérifiez le résultat avec un court enregistrement.

## Licence

MIT. Consultez le fichier `LICENSE`.
