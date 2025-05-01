# main.py
import subprocess

subprocess.run(["pip", "install", "-r", "requirements.txt"])

subprocess.run(["streamlit", "run", "UI.py"])
