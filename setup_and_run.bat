@echo off
echo Création de l'environnement virtuel...
python -m venv venv
call venv\Scripts\activate

echo Installation des dépendances...
pip install --upgrade pip
pip install -r requirements.txt

echo Lancement de l'application Streamlit...
streamlit run UI.py
pause

