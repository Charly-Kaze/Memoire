# Memoire
# Générateur de Rapport Sprint JIRA

Cette application permet de générer un **rapport PDF** contenant les tickets d’un sprint clos sur JIRA, à l’aide d’une interface web accessible depuis un **téléphone ou un ordinateur**, via **Streamlit**.

---

## Fonctionnalités

- Connexion à JIRA via API
- Sélection automatique du dernier sprint clos
- Extraction et affichage des tickets
- Génération d’un **fichier PDF** contenant :
  - Clé du ticket
  - Résumé
  - Statut
  - Assignee
- Interface simple via navigateur, utilisable depuis mobile
- Téléchargement direct du PDF

---

## Lancement (Windows)

1. **Cloner ce projet** :
   ```bash
   git clone https://github.com/Charly-Kaze/Memoire.git
   cd Memoire
2. **Lancer le script d’installation et d’exécution** :
   ```bash
   setup_and_run.bat
