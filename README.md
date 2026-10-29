**# Guide complet — Automatisation des cours Google Meet**



Bienvenue ! Ce guide explique, étape par étape, comment installer et utiliser le script d’automatisation des cours en ligne.



L’objectif est simple : **\*\*rejoindre automatiquement un cours Google Meet, démarrer l’enregistrement avec OBS Studio, arrêter l’enregistrement à la fin du cours et quitter la réunion.\*\***



Aucune connaissance en programmation n’est nécessaire pour suivre ce guide. Prenez le temps de lire chaque étape dans l’ordre.



\> **\*\*Important :\*\*** le script ne remplace pas la vérification de votre présence en cours. Testez-le avant de compter sur lui pour une séance importante. Respectez les règles de votre établissement et obtenez l’autorisation nécessaire avant d’enregistrer ou de partager les cours.



\---



**## Sommaire**



1\. Ce qu’il faut avant de commencer

2\. Télécharger et installer OBS Studio

3\. Télécharger le projet

4\. Installer Python

5\. Préparer le dossier du projet

6\. Configurer OBS pour l’enregistrement

7\. Activer la connexion entre OBS et le script

8\. Préparer son emploi du temps

9\. Lancer le script

10\. Vérifier que tout fonctionne

11\. Retrouver ses enregistrements

12\. Transcription automatique des cours

13\. Résoudre les problèmes courants

14\. Arrêter le script correctement

15\. Sécurité et bonnes pratiques



\---



**## 1. Ce qu’il faut avant de commencer**



Préparez les éléments suivants :



\- Un ordinateur Windows 10 ou Windows 11.

\- Une connexion Internet stable.

\- Un compte Google permettant d’accéder aux réunions de cours.

\- OBS Studio, le logiciel qui réalisera les enregistrements.

\- Python, nécessaire au fonctionnement du script.

\- Le dossier du projet et son fichier de configuration.

\- Les liens Google Meet et les horaires exacts de vos cours.



Prévoyez également suffisamment d’espace libre sur votre disque : les fichiers vidéo peuvent occuper beaucoup de place.



**\*\*Comment fonctionne le système ?\*\***



1\. Le script surveille les horaires configurés.

2\. À l’heure du cours, il ouvre le lien Google Meet.

3\. Il essaie de rejoindre la réunion sans activer le microphone ni la caméra.

4\. Si la participation est confirmée, il demande à OBS de commencer l’enregistrement.

5\. À la fin du cours, il arrête l’enregistrement et essaie de quitter la réunion.



Le bon fonctionnement dépend notamment de la configuration d’OBS, de l’accès à Google Meet et de la disponibilité de l’ordinateur.



\---



**## 2. Télécharger et installer OBS Studio**



OBS Studio est le logiciel utilisé pour enregistrer la vidéo.



**### Étape 1 — Télécharger le logiciel**



Ouvrez le lien officiel :



**\*\*https\://obsproject.com/fr/download\*\***



1\. Choisissez Windows.

2\. Téléchargez l’installateur proposé.

3\. Ouvrez le fichier téléchargé.

4\. Suivez les étapes de l’installation.

5\. Ouvrez OBS Studio.



N’utilisez pas de sites de téléchargement non officiels.



**### Étape 2 — Premier démarrage**



Au premier lancement, OBS peut proposer un assistant de configuration automatique.



Vous pouvez suivre ses recommandations, puis terminer la configuration.



Ne fermez pas OBS définitivement : il devra être ouvert lorsque le script fonctionnera.



\---



**## 3. Télécharger le projet**



Récupérez le dossier du projet depuis le dépôt GitHub fourni par la personne qui partage le script.



**\*\*Lien du dépôt :\*\*** [https\://github.com/thiamyatma/rec-cours-automation]



Si vous débutez, la méthode la plus simple est de télécharger le projet sous forme de fichier ZIP depuis GitHub, puis de l’extraire dans un dossier facile à retrouver, par exemple :



\`C:\Cours-Automatiques\`



Si le projet vous a déjà été transmis sous forme de dossier, utilisez directement ce dossier.



**### Vérification**



Ouvrez le dossier du projet. Il doit contenir notamment le fichier :



\`automation.py\`



Il peut également contenir \`config.json\`, \`requirements.txt\` et d’autres fichiers nécessaires.



**\*\*Ne publiez pas votre fichier \`config.json\` s’il contient votre mot de passe OBS ou des liens privés de cours.\*\***



\---



**## 4. Installer Python**



Python est le langage utilisé par le script.



**### Étape 1 — Télécharger Python**



Téléchargez Python depuis le site officiel :



https\://www\.python.org/downloads/windows/



Choisissez une version compatible avec les dépendances du projet.



**### Étape 2 — Installer Python**



Pendant l’installation, si l’option **\*\*Add Python to PATH\*\*** est proposée, cochez-la, puis terminez l’installation.



**### Étape 3 — Vérifier l’installation**



1\. Appuyez sur \`Windows + R\`.

2\. Saisissez \`powershell\`.

3\. Appuyez sur Entrée.

4\. Tapez :



\`\`\`powershell

python --version

\`\`\`



Si une version de Python s’affiche, continuez.



Si Windows indique que Python est introuvable, vérifiez l’installation ou essayez :



\`\`\`powershell

py --version

\`\`\`



\---



**## 5. Préparer le dossier du projet**



Ouvrez PowerShell dans le dossier où se trouve \`automation.py\`.



Une méthode simple consiste à ouvrir ce dossier dans l’Explorateur de fichiers, à cliquer dans la barre d’adresse, à taper \`powershell\`, puis à appuyer sur Entrée.



**### Étape 1 — Créer un environnement Python**



Copiez cette commande :



\`\`\`powershell

python -m venv .venv

\`\`\`



Si la commande \`python\` ne fonctionne pas, essayez \`py\` à la place.



**### Étape 2 — Installer les dépendances**



Si le dossier contient un fichier \`requirements.txt\`, exécutez :



\`\`\`powershell

.\\.venv\Scripts\python.exe -m pip install -r requirements.txt

\`\`\`



Si ce fichier est absent, demandez au responsable du projet la liste officielle des dépendances et leurs versions. Ne devinez pas les paquets à installer.



Le script utilise notamment Playwright pour contrôler le navigateur et \`obsws-python\` pour communiquer avec OBS.



Si Playwright est installé mais que son navigateur Chromium n’est pas encore disponible, la commande suivante peut être nécessaire :



\`\`\`powershell

.\\.venv\Scripts\python.exe -m playwright install chromium

\`\`\`



\---



**## 6. Configurer OBS pour enregistrer le cours**



C’est une étape essentielle : le script peut démarrer un enregistrement, mais OBS doit être configuré pour capturer le contenu souhaité.



**### Étape 1 — Créer une scène**



Dans OBS :



1\. Repérez le panneau **\*\*Scènes\*\***.

2\. Cliquez sur le bouton \`+\`.

3\. Donnez un nom à la scène, par exemple \`Cours\`.

4\. Validez.



**### Étape 2 — Ajouter une source vidéo**



Dans le panneau **\*\*Sources\*\*** :



1\. Cliquez sur \`+\`.

2\. Choisissez une source adaptée, par exemple **\*\*Capture d’écran\*\*** ou **\*\*Capture de fenêtre\*\***, selon ce que vous souhaitez enregistrer.

3\. Suivez les instructions affichées.

4\. Vérifiez que l’aperçu montre bien le contenu attendu.



Si l’aperçu est noir, corrigez ce problème avant de continuer.



**### Étape 3 — Vérifier le son**



Si vous souhaitez enregistrer le son du cours :



1\. Vérifiez que le son de l’ordinateur est disponible dans OBS.

2\. Regardez l’indicateur correspondant dans le **\*\*Mélangeur audio\*\***.

3\. Lancez un court enregistrement manuel.

4\. Écoutez le fichier obtenu pour vérifier que le son est présent.



La configuration audio peut varier d’un ordinateur à l’autre. Ne supposez pas que le son fonctionne simplement parce que l’image est visible.



**### Étape 4 — Choisir le dossier de destination**



Dans OBS :



1\. Ouvrez **\*\*Paramètres\*\***.

2\. Allez dans **\*\*Sortie\*\***.

3\. Repérez le chemin d’enregistrement.

4\. Choisissez un dossier facile à retrouver, avec suffisamment d’espace libre.

5\. Cliquez sur **\*\*Appliquer\*\***, puis sur **\*\*OK\*\***.



Le script utilise le dossier défini dans OBS. Les noms des fichiers sont générés automatiquement à partir de la date et du nom du cours.



\---



**## 7. Activer la connexion entre OBS et le script**



Le script doit pouvoir envoyer des commandes à OBS pour démarrer et arrêter les enregistrements.



**### Étape 1 — Ouvrir les paramètres WebSocket**



Dans OBS, ouvrez le menu **\*\*Outils\*\***, puis cherchez les paramètres du serveur WebSocket.



Selon la version d’OBS, le libellé peut légèrement varier.



**### Étape 2 — Activer le serveur**



1\. Activez le serveur WebSocket.

2\. Repérez le port indiqué.

3\. Activez l’authentification par mot de passe si elle est proposée.

4\. Définissez un mot de passe fort.

5\. Enregistrez les paramètres.



Pour les versions récentes d’OBS, le port WebSocket par défaut est généralement \`4455\`. Utilisez toutefois le port réellement affiché dans vos paramètres.



**### Étape 3 — Reporter les informations dans \`config.json\`**



Le fichier de configuration contient les informations de connexion à OBS.



Exemple de structure :



\`\`\`json

{

  "host": "127.0.0.1",

  "port": 4455,

  "password": "VOTRE_MOT_DE_PASSE_OBS",

  "sessions": []

}

\`\`\`



Cet exemple illustre uniquement la structure générale : il ne remplace pas votre configuration complète.



\- \`host\` : adresse de l’ordinateur sur lequel OBS fonctionne.

\- \`port\` : port du serveur WebSocket.

\- \`password\` : mot de passe défini dans OBS.

\- \`sessions\` : liste des cours à automatiser.



**\*\*Ne partagez jamais votre vrai mot de passe dans un groupe, une capture d’écran ou un dépôt public.\*\*** Chaque utilisateur doit configurer ses propres informations.



\---



**## 8. Préparer son emploi du temps**



Le script lit les cours configurés dans \`config.json\`. Chaque cours doit comporter les informations attendues par le programme :



\- \`name\` : nom du cours.

\- \`days\` : jours de la semaine.

\- \`start\` : heure de début au format \`HH:MM\`.

\- \`end\` : heure de fin au format \`HH:MM\`.

\- \`meet_url\` : lien Google Meet.



Exemple de cours fictif :



\`\`\`json

{

  "name": "Cours de test",

  "days": [0],

  "start": "09:00",

  "end": "10:00",

  "meet_url": "https\://meet.google.com/xxx-yyyy-zzz"

}

\`\`\`



Dans cet exemple, le cours est prévu le lundi, de 9 h à 10 h.



**\*\*Correspondance des jours :\*\***



\| Valeur | Jour |

\|---:|---|

\| \`0\` | Lundi |

\| \`1\` | Mardi |

\| \`2\` | Mercredi |

\| \`3\` | Jeudi |

\| \`4\` | Vendredi |

\| \`5\` | Samedi |

\| \`6\` | Dimanche |



Si un cours a lieu plusieurs jours, indiquez plusieurs valeurs. Par exemple, \`[0, 2]\` correspond au lundi et au mercredi.



Les heures doivent être écrites au format de 24 heures. Écrivez \`14:30\`, et non \`2:30 PM\`.



**### Attention aux dates**



Le programme possède également des dates de début et de fin définies dans \`automation.py\`.



La configuration doit donc être cohérente avec la période prévue. Si ces dates sont dépassées ou incorrectes, le script peut ne pas lancer les cours attendus.



Si vous ne savez pas modifier ces paramètres, demandez au responsable du projet de vous fournir une version déjà configurée.



**### Attention aux liens privés**



Chaque étudiant doit utiliser les liens correspondant à ses propres cours et vérifier que son compte Google a le droit d’accéder aux réunions.



\---



**## 9. Lancer le script**



Avant de lancer le programme, vérifiez les points suivants :



\- OBS Studio est ouvert.

\- Le serveur WebSocket est activé.

\- Le mot de passe et le port correspondent à ceux de \`config.json\`.

\- Les cours et leurs horaires sont correctement renseignés.

\- Le navigateur peut accéder à Google Meet.

\- L’ordinateur ne va pas se mettre en veille pendant un cours.



**### Étape 1 — Ouvrir PowerShell dans le dossier du projet**



Placez-vous dans le dossier contenant \`automation.py\`.



**### Étape 2 — Lancer le mode programmé**



Exécutez :



\`\`\`powershell

.\\.venv\Scripts\python.exe .\automation.py

\`\`\`



Laissez la fenêtre PowerShell ouverte.



Le programme surveille les créneaux configurés. Selon les horaires et la période définie, il peut rester en attente avant le prochain cours.



Ne fermez pas PowerShell et ne mettez pas l’ordinateur en veille pendant le fonctionnement du script.



**### Étape 3 — Première connexion à Google Meet**



Lors de la première utilisation, le navigateur peut demander de vous connecter à votre compte Google.



Connectez-vous vous-même, puis vérifiez que le compte peut accéder à la réunion prévue.



Le script utilise un profil de navigateur local. Ne partagez pas le dossier \`profil_google_meet\`, car il peut contenir des données de session.



\---



**## 10. Vérifier que tout fonctionne**



Ne découvrez pas le jour d’un examen que votre configuration est incorrecte.



Effectuez d’abord un test avec une réunion de test que vous contrôlez.



**### Liste de vérification**



\- [ ] OBS s’ouvre correctement.

\- [ ] L’aperçu OBS affiche le contenu attendu.

\- [ ] Le son du cours est audible dans un enregistrement de test.

\- [ ] Le script se connecte à OBS sans erreur.

\- [ ] Le navigateur ouvre le lien Google Meet.

\- [ ] La participation à la réunion est confirmée.

\- [ ] L’enregistrement démarre.

\- [ ] Le fichier vidéo est créé.

\- [ ] L’enregistrement s’arrête à la fin.

\- [ ] Le navigateur quitte la réunion lorsque la fonction de sortie automatique fonctionne correctement.



Vérifiez le fichier enregistré en le lisant jusqu’au bout. La présence d’un fichier ne garantit pas à elle seule que l’image et le son sont corrects.



\---



**## 11. Retrouver ses enregistrements**



Les vidéos sont enregistrées dans le dossier de destination défini dans OBS.



Le nom du fichier contient normalement la date, le nom du cours et l’heure de début.



Exemple fictif :



\`2026-10-30_Cours-de-test_09-00\`



Selon les paramètres d’OBS, l’extension peut être \`.mkv\`, \`.mp4\` ou un autre format configuré.



Pour chaque cours, vérifiez que le fichier existe et qu’il peut être lu.



**\*\*Conseil :\*\*** conservez assez d’espace disque et transférez régulièrement les vidéos que vous souhaitez garder vers un emplacement sécurisé.



\---



**## 12. Transcription automatique des cours**

Le projet peut utiliser `transcription.py` et Faster-Whisper pour transcrire localement les enregistrements audio et vidéo, sans utiliser d’API payante. Les transcriptions peuvent ensuite être envoyées manuellement à Claude pour produire des résumés, des fiches de révision ou des questions d’entraînement.

**### Prérequis**

- Le fichier `transcription.py` doit être présent dans le dossier du projet.
- Les dépendances doivent être installées dans l’environnement virtuel.
- FFmpeg doit être installé et accessible depuis PowerShell.
- Le dossier de destination des enregistrements doit correspondre à la valeur `RECORDINGS_DIR` définie dans `transcription.py`.

Si `faster-whisper` n’est pas encore dans `requirements.txt`, ajoutez cette ligne :

```text
faster-whisper
```

Puis installez les dépendances :

```powershell
.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt
```

Au premier lancement, Faster-Whisper peut télécharger le modèle de transcription. Une connexion Internet et suffisamment d’espace disque sont donc nécessaires.

**### Transcrire les fichiers déjà présents**

Depuis PowerShell, dans le dossier du projet, lancez :

```powershell
.\\.venv\\Scripts\\python.exe .\\transcription.py --once
```

Le script analyse les enregistrements disponibles puis se termine.

**### Surveiller automatiquement le dossier**

Pour surveiller continuellement le dossier des enregistrements et traiter les nouveaux fichiers, lancez :

```powershell
.\\.venv\\Scripts\\python.exe .\\transcription.py
```

Le script vérifie périodiquement le dossier configuré dans `RECORDINGS_DIR`. Les fichiers texte sont enregistrés dans le sous-dossier `transcriptions` du dossier surveillé. Les fichiers déjà transcrits sont normalement ignorés si le fichier texte correspondant existe déjà.

**### Utiliser les transcriptions avec Claude**

1. Ouvrez le fichier `.txt` généré dans le dossier `transcriptions`.
2. Vérifiez que la transcription est lisible et suffisamment complète.
3. Envoyez le texte à Claude avec vos consignes pour obtenir un résumé, une fiche de révision ou des exercices.

La transcription automatique peut contenir des erreurs, notamment lorsque le son est faible, que plusieurs personnes parlent en même temps ou que le vocabulaire technique est spécialisé. Vérifiez les notions importantes avant d’utiliser le texte pour réviser.

**### Important**

La transcription doit être testée avec un enregistrement court avant une séance importante. Vérifiez que le chemin `RECORDINGS_DIR` correspond réellement au dossier où OBS enregistre les fichiers. Si la transcription est lancée séparément, elle ne démarre pas automatiquement avec `automation.py`. Cette intégration nécessite que le code de lancement du service soit effectivement présent dans `automation.py`.

---

**## 13. Résoudre les problèmes courants**



**### Problème : Python n’est pas reconnu**



**\*\*Solution :\*\*** vérifiez l’installation de Python et essayez :



\`\`\`powershell

py --version

\`\`\`



**### Problème : le script ne se connecte pas à OBS**



Vérifiez :



1\. Qu’OBS est ouvert.

2\. Que le serveur WebSocket est activé.

3\. Que le port dans \`config.json\` est correct.

4\. Que le mot de passe correspond exactement à celui d’OBS.



**### Problème : Google Meet ne rejoint pas la réunion**



Vérifiez que :



\- Le lien est valide.

\- Le compte Google utilisé possède les autorisations nécessaires.

\- L’organisateur a autorisé votre participation si elle doit être approuvée.

\- Le navigateur n’affiche pas une fenêtre bloquant la progression.



**### Problème : OBS enregistre une image noire**



Vérifiez la source de capture et les autorisations de Windows. Essayez une capture de fenêtre ou une capture d’écran adaptée à votre ordinateur, puis effectuez un nouvel enregistrement de test.



**### Problème : la vidéo n’a pas de son**



Vérifiez les sources audio et les indicateurs du mélangeur OBS. Faites un court test et écoutez le fichier avant le prochain cours.



**### Problème : l’enregistrement ne démarre pas à l’heure prévue**



Vérifiez les horaires, les jours de la semaine, les dates de début et de fin du script ainsi que l’heure de Windows.



Le script ne peut pas lancer un cours si le programme est fermé, si l’ordinateur est en veille ou si la réunion ne peut pas être rejointe.



**### Problème : Google Meet reste ouvert après le cours**



Vérifiez que la version du script contient la fonction de sortie automatique et que le journal confirme la tentative de quitter la réunion.



Si le bouton de sortie n’est pas détecté, la langue ou l’interface de Google Meet peut nécessiter une adaptation.



**### Problème : aucune transcription n’est créée**

Vérifiez que `transcription.py` existe, que `RECORDINGS_DIR` pointe vers le bon dossier, que le fichier audio ou vidéo est terminé et que Faster-Whisper ainsi que FFmpeg sont installés. Lancez d’abord le script avec `--once` pour voir les éventuels messages d’erreur.

**### Où consulter les erreurs ?**



Le projet écrit ses messages dans :



\`automation.log\`



En cas de problème, transmettez au responsable du projet les messages d’erreur pertinents, en masquant les liens privés, les mots de passe et toute donnée personnelle.



\---



**## 14. Arrêter le script correctement**



Pour interrompre volontairement le programme :



1\. Revenez à la fenêtre PowerShell où il tourne.

2\. Appuyez sur \`Ctrl + C\`.

3\. Attendez que le programme termine son arrêt.

4\. Vérifiez qu’OBS n’enregistre plus.

5\. Vérifiez que la réunion a été quittée.



Le comportement exact dépend de l’état du programme au moment de l’interruption. Après tout arrêt, vérifiez toujours qu’OBS n’est plus en train d’enregistrer.



Ne supprimez pas les fichiers vidéo tant que vous n’avez pas vérifié que vous possédez les enregistrements nécessaires.



\---



**## 15. Sécurité et bonnes pratiques**



Pour utiliser ce projet dans de bonnes conditions :



\- N’enregistrez pas un cours sans respecter les règles de l’établissement et les droits des participants.

\- Ne partagez pas les vidéos sans autorisation.

\- Protégez les identifiants Google et le mot de passe WebSocket d’OBS.

\- Ne publiez pas \`config.json\` si ce fichier contient des secrets ou des liens privés.

\- Ne partagez pas le profil de navigateur local.

\- Gardez une copie de sauvegarde des fichiers importants.

\- Vérifiez régulièrement que les enregistrements contiennent bien l’image et le son.

\- Gardez à l’esprit que l’automatisation peut échouer si Google Meet, Windows, OBS ou la connexion Internet rencontre un problème.



\---



**## En résumé**



Pour bénéficier du script :



1\. Installez OBS Studio et Python.

2\. Téléchargez le projet et installez ses dépendances.

3\. Configurez OBS pour enregistrer l’image et le son souhaités.

4\. Activez le serveur WebSocket et renseignez les informations de connexion.

5\. Configurez votre emploi du temps et vos liens Google Meet.

6\. Lancez le script et gardez l’ordinateur éveillé.

7\. Faites un test complet avant de compter sur l’automatisation pour vos cours.
8\. Si vous utilisez la transcription, testez `transcription.py` et vérifiez les fichiers texte générés.



**\*\*Un dernier conseil :\*\*** si vous n’êtes pas à l’aise avec la configuration, demandez au responsable du projet de vous aider à préparer \`config.json\`. Une configuration correcte dès le départ est plus simple et plus fiable que de corriger les erreurs pendant un cours.
