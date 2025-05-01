from jira import JIRA
from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Rapport de Sprint", ln=True, align="C")
        self.ln(10)

    def issue_block(self, issue):
        self.set_font("Arial", "B", 10)
        self.cell(0, 8, f"{issue.key}: {issue.fields.summary}", ln=True)
        self.set_font("Arial", "", 9)
        assignee = getattr(issue.fields.assignee, 'displayName', 'Non assigné')
        self.multi_cell(0, 6, f"Status: {issue.fields.status.name} | Assignee: {assignee}")
        self.ln(2)

def generer_rapport():
    # Connexion à JIRA
    email = "charlykaze88@gmail.com"
    api_token ="ATATT3xFfGF0O3VWjGYRiSmS4EOBWK65yPMBD58zvsSlp8xKwc7Zc_xSnC5BcYX_8YtVd8vVaWGzejnfnaU0ioCO1ZSgDK7SYl_8C8tHGK1qxfG6PeMLaJVfaNwT6mDEnc_Xv7tnLrTSb7InMspMsrehcAeX7sJaEixjLMGZwTxPQcZp3IHBig8=A33E42BF"
    server = "https://charlykaze88.atlassian.net"

    jira = JIRA(server=server, basic_auth=(email, api_token))

    # Sélection du sprint à exporter
    board_id = 2
    sprints = jira.sprints(board_id)
    sprint_clos = [s for s in sprints if s.state == "closed"]
    if not sprint_clos:
        print("Aucun sprint clos trouvé.")
        return
    
    dernier_sprint = sprint_clos[-1]  # Dernier sprint clos
    sprint_id = dernier_sprint.id

    # Requête JQL
    jql = f"sprint = {sprint_id} ORDER BY priority DESC"
    issues = jira.search_issues(jql, maxResults=1000)

    # Génération PDF
    pdf = PDF()
    pdf.add_page()
    for issue in issues:
        pdf.issue_block(issue)

    chemin_pdf = os.path.join(os.getcwd(), "rapport_sprint.pdf")
    pdf.output(chemin_pdf)
    print("Rapport PDF généré :", chemin_pdf)
