from app.project_data import ProjectData
from rich import print

def run_sync_tasks(data: ProjectData):
    """
    Executa um conjunto de ações de sincronização quando a flag needs_sync está ativa.
    Este módulo centraliza as tarefas automáticas acionadas por mudanças no banco.
    """
    if data.needs_sync:
        print("\n[bold yellow]>> Detectadas alterações pendentes. Sincronizando relatórios...[/bold yellow]")
        
        # Ação 1: Atualizar o arquivo Project Report.md
        data.report_projeto()
        
        # Reseta a variável de controle
        data.needs_sync = False
        
        # Salva o estado final no banco de dados
        data.save()
        print("[bold green]Tudo pronto: Todos os relatórios foram atualizados e sincronizados.[/bold green]\n")
