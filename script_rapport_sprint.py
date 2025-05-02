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


def get_sprint_max(jira, board_id=2):
    sprints = jira.sprints(board_id)
    sprint_numeros = [int(s.name.split()[-1]) for s in sprints if s.name.split()[-1].isdigit()]
    return max(sprint_numeros)


def generer_rapport(sprint_num):
    email = os.getenv("JIRA_EMAIL")
    api_token = os.getenv("JIRA_API_TOKEN")
    server = "https://charlykaze88.atlassian.net"
    board_id = 2

    jira = JIRA(server=server, basic_auth=(email, api_token))

    sprints = jira.sprints(board_id)
    sprint_match = [s for s in sprints if s.name.endswith(str(sprint_num))]

    if not sprint_match:
        return None, "Sprint introuvable"

    sprint_id = sprint_match[0].id
    jql = f"sprint = {sprint_id} ORDER BY priority DESC"
    issues = jira.search_issues(jql, maxResults=1000)

    pdf = PDF()
    pdf.add_page()
    for issue in issues:
        pdf.issue_block(issue)

    filename = f"rapport_sprint_{sprint_num}.pdf"
    chemin_pdf = os.path.join(os.getcwd(), filename)
    pdf.output(chemin_pdf)
    return filename, None
