from app.project_data import ProjectData
from datetime import datetime

data = ProjectData.load_or_create()
data.add_works(description="Melhoria no formato do relatório Markdown", time=0.5, work_date=datetime.now().strftime("%Y-%m-%d"))
data.save()
data.report_projeto()
print("Trabalho adicionado e relatório gerado.")
