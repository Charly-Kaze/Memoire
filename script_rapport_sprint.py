from jira import JIRA
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from fpdf import FPDF
import os

# --- Paramètres de connexion ---
email = "charlykaze88@gmail.com"
api_token = "ATATT3xFfGF0vgpVUChEQpmsYqxeTRnPtDDRKd-z9AUalN5kHWFHZgrJTBYDQ50Ml7FoyrxKSDowtYZaPTKQvva_kSqS3jQeLrXdovSnfnt1QanFwILmvMFknp49rO0OY03O538zHzRJOWag9OUGFRH1L6lasFeM4NeEe5kw4ljYSiCezr3jf8I=7CB3F2DE"
server = "https://charlykaze88.atlassian.net"

jira = JIRA(server=server, basic_auth=(email, api_token))

# ID du tableau Scrum/Board (visible dans l'URL de ton projet)
board_id = 2  # remplace par le bon ID

# Récupération de tous les sprints du board
sprints = jira.sprints(board_id)
print(sprints)

# Affichage des sprints clos uniquement
for sprint in sprints:
    if sprint.state == 'closed':
        print(f"Sprint clos trouvé → ID: {sprint.id} | Nom: {sprint.name}")

sprint_id = 1
jql = f"sprint = {sprint_id} ORDER BY priority DESC"
issues = jira.search_issues(jql, maxResults=1000)
print(issues)

# Étape 4 : Générer un rapport PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Rapport de Sprint", ln=True, align="C")
        self.ln(10)
    
    def issue_block(self, issue):
        self.set_font("Arial", "B", 10)
        self.cell(0, 8, f"{issue.key}: {issue.fields.summary}", ln=True)
        self.set_font("Arial", "", 9)
        self.multi_cell(0, 6, f"Status: {issue.fields.status.name} | Assignee: {getattr(issue.fields.assignee, 'displayName', 'Non assigné')}")
        self.ln(2)

pdf = PDF()
pdf.add_page()

for issue in issues:
    pdf.issue_block(issue)

chemin_pdf = os.path.join(os.getcwd(), "rapport_sprint.pdf")
pdf.output(chemin_pdf)
print("Rapport PDF généré :", chemin_pdf)
