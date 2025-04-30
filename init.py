# main.py
import subprocess

subprocess.run(["pip", "install", "-r", "requirements.txt"])

streamlit run UI.py
