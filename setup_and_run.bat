@echo off
echo Création de l'environnement virtuel...
python -m venv venv
call venv\Scripts\activate

echo Installation des dépendances...
python -m pip install requirements.txt

echo Lancement de l'application Streamlit...
streamlit run UI.py
pause

