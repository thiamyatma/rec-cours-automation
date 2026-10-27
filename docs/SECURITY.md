
# Sécurité du projet

Avant chaque publication :

- Vérifier que `config.json` n'est pas suivi par Git.
- Ne jamais publier le mot de passe OBS.
- Ne jamais publier le profil Chromium, les cookies ou les données de connexion Google.
- Ne jamais publier les vidéos de cours ou les journaux contenant des informations privées.
- Vérifier les fichiers avec `git status` avant chaque envoi.

Si un secret est publié accidentellement, considérez-le compromis et changez-le immédiatement. Supprimer le fichier dans un commit ultérieur ne suffit pas à effacer son historique.

Chaque utilisateur doit utiliser son propre profil Google, son instance OBS et ses propres liens de réunion.
