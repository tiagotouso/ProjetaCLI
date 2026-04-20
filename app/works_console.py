from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from app.project_data import ProjectData, get_db_dir
from app.models import StatusEnum
from rich import print
from rich.table import Table
from rich import box
import typer
import re
from datetime import date
from pathlib import Path
from typing import Optional

def _check_init():
    if not (get_db_dir() / 'db.json').exists():
        print(f"[red]Erro: Projeto não inicializado. Execute [yellow]proj project init[/yellow] primeiro.[/red]")
        return False
    return True

def work_add():
    if not _check_init(): return
    data = ProjectData.load_or_create()
    
    if not data.milestones and not data.issues:
        print("[yellow]Não há marcos ou issues para registrar trabalho.[/yellow]")
        return

    # 1. Action ou Issue?
    type_choice = inquirer.select(
        message="O trabalho é sobre:",
        choices=[
            Choice("action", "Uma Ação do Projeto"),
            Choice("issue", "Uma Issue (Problema/Impedimento)")
        ]
    ).execute()
    
    idaction = None
    idissue = None
    
    if type_choice == "action":
        # Filtrar marcos não concluídos nem cancelados
        milestones = [m for m in data.milestones if m.status not in [StatusEnum.CONCLUIDO, StatusEnum.CANCELADO]]
        
        if not milestones:
            print("[yellow]Nenhum marco ativo encontrado. Registre em uma Issue ou ative um marco.[/yellow]")
            return
            
        m_choice = inquirer.select(
            message="Selecione o Marco:",
            choices=[Choice(m.idmilestone, f"{m.status.value} {m.name}") for m in milestones]
        ).execute()
        
        # Ações desse marco
        actions = [a for a in data.actions if a.idmilestone == m_choice and a.status != StatusEnum.CONCLUIDO]
        
        if not actions:
            print("[yellow]Nenhuma ação pendente neste marco.[/yellow]")
            return
            
        idaction = inquirer.select(
            message="Selecione a Ação:",
            choices=[Choice(a.idaction, f"{a.status.value} {a.name}") for a in actions]
        ).execute()
        
    else:
        # Issues
        issues = [i for i in data.issues if i.status != StatusEnum.CONCLUIDO]
        if not issues:
            print("[yellow]Nenhuma issue aberta encontrada.[/yellow]")
            return
            
        idissue = inquirer.select(
            message="Selecione a Issue:",
            choices=[Choice(i.idissues, f"{i.status.value} {i.description[:50]}") for i in issues]
        ).execute()

    # Detalhes do trabalho
    description = inquirer.text(message="Descrição do que foi feito:").execute()
    time_str = inquirer.text(message="Tempo gasto (horas):", default="1").execute()
    try:
        time_val = float(time_str)
    except ValueError:
        print("[red]Tempo inválido. Usando 0.0[/red]")
        time_val = 0.0
        
    work_date = inquirer.text(message="Data (AAAA-MM-DD):", default=date.today().isoformat()).execute()
    
    data.add_works(description, time_val, work_date, idaction=idaction, idissue=idissue)
    data.save()
    print("[green]Worklog registrado com sucesso![/green]")

def work_list():
    if not _check_init(): return
    data = ProjectData.load_or_create()
    if not data.works:
        print("[yellow]Nenhum registro de trabalho encontrado.[/yellow]")
        return
        
    table = Table(box=box.MINIMAL, header_style="bold magenta")
    table.add_column("ID", width=10)
    table.add_column("DATA", width=12)
    table.add_column("TIPO", width=8)
    table.add_column("REF", width=30)
    table.add_column("DESCRIÇÃO", width=40)
    table.add_column("HORAS", justify="right")
    
    for w in sorted(data.works, key=lambda x: x.date, reverse=True):
        ref_name = "-"
        tipo = ""
        if w.idaction:
            tipo = "Ação"
            a = data.get_action_by_code(w.idaction)
            if a: ref_name = a.name
        elif w.idissue:
            tipo = "Issue"
            i = data.get_issue_by_code(w.idissue)
            if i: ref_name = i.description[:30]
            
        table.add_row(w.idwork[:8], w.date, tipo, ref_name, w.description, f"{w.time}h")
    
    print(table)
    total_h = sum(w.time for w in data.works)
    print(f"\n[bold cyan]TOTAL DE HORAS TRABALHADAS: {total_h}h[/bold cyan]")

def work_delete(id_prefix: str):
    if not _check_init(): return
    data = ProjectData.load_or_create()
    works = [w for w in data.works if w.idwork.startswith(id_prefix)]
    if not works:
        print("[red]Registro não encontrado.[/red]")
        return
    
    w = works[0]
    if typer.confirm(f"Excluir registro '{w.description[:30]}...' ({w.time}h)?"):
        data.del_work(w.idwork)
        data.save()
        print("[green]Registro excluído.[/green]")

def work_sync():
    """Importa tags do worklogs.md para o banco de dados e atualiza o arquivo com os IDs."""
    if not _check_init(): return
    data = ProjectData.load_or_create()
    sync_path = get_db_dir() / 'worklogs.md'
    if not sync_path.exists():
        print("[yellow]Arquivo worklogs.md não encontrado.[/yellow]")
        return

    txt = sync_path.read_text(encoding='utf-8')
    lines = txt.split('\n')
    new_lines = []
    current_action_id = None
    current_issue_id = None
    mudou = False

    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            new_lines.append(line)
            continue

        # Identificar se a linha é uma Ação ou Issue pelo ID no comentário
        id_match = re.search(r"<!-- \[(.*?)\] -->", line_strip)
        if id_match:
            ref_id = id_match.group(1)
            # Verifica se é ação ou issue no banco para saber onde vincular
            if any(a.idaction == ref_id for a in data.actions):
                current_action_id = ref_id
                current_issue_id = None
            else:
                current_issue_id = ref_id
                current_action_id = None
            new_lines.append(line)
            continue

        # Identificar se é uma tag de trabalho: > DATA HORA DESCRIÇÃO <!-- [ID_TRABALHO] -->
        # Regex flexível para capturar ID no início [id] ou no fim <!-- [id] -->
        tag_match = re.search(r"^>\s*(?:\[(?P<id_start>[a-f0-9-]+)\]\s*)?(?P<date>\S+)\s+(?P<time>\d*\.?\d+)\s+(?P<desc>.*?)(?:\s*<!-- \[(?P<id_end>[a-f0-9-]+)\] -->)?$", line_strip)
        
        # Só processamos o quote se ele tiver o padrão de data hora descriçao e estiver abaixo de uma ref
        if tag_match and (current_action_id or current_issue_id):
            work_id = tag_match.group('id_end') or tag_match.group('id_start')
            w_date = tag_match.group('date')
            try:
                w_time = float(tag_match.group('time'))
            except ValueError:
                new_lines.append(line)
                continue
            w_desc = tag_match.group('desc').strip()

            if not work_id:
                # Novo registro! Verificar duplicidade manual no banco
                is_duplicate = False
                for w in data.works:
                    # Checagem rigorosa para evitar duplicar o mesmo registro
                    if (w.idaction == current_action_id and 
                        w.idissue == current_issue_id and 
                        w.date == w_date and 
                        abs(w.time - w_time) < 0.01 and 
                        w.description == w_desc):
                        is_duplicate = True
                        work_id = w.idwork
                        break
                
                if not is_duplicate:
                    data.add_works(w_desc, w_time, w_date, idaction=current_action_id, idissue=current_issue_id)
                    work_id = data.works[-1].idwork
                    mudou = True
                
                # Montar a nova linha já com o ID no final para o arquivo
                new_line = f"  > {w_date} {w_time} {w_desc} <!-- [{work_id}] -->"
                new_lines.append(new_line)
                mudou = True # Indica que o arquivo deve ser reescrito
            else:
                # Se já tinha ID (no início ou fim), garantimos que fique no final agora
                new_line = f"  > {w_date} {w_time} {w_desc} <!-- [{work_id}] -->"
                if new_line != line:
                    mudou = True
                new_lines.append(new_line)
        else:
            # Se encontrar uma linha que não é quote, e não é a linha do ID, perdemos o contexto da referência
            if not line_strip.startswith(">"):
                current_action_id = None
                current_issue_id = None
            new_lines.append(line)

    if mudou:
        data.save()
        sync_path.write_text("\n".join(new_lines), encoding='utf-8')
        print("[green]Sincronização de trabalhos concluída com sucesso![/green]")
    else:
        print("[blue]Nenhum novo registro de trabalho detectado.[/blue]")

def work_report():
    if not _check_init(): return
    data = ProjectData.load_or_create()
    
    report_path = Path("Worklog_Report.md")
    content = f"# Relatório de Trabalho - {data.project.name}\n\n"
    content += f"Data de Emissão: {date.today().isoformat()}\n\n"
    
    total_h = sum(w.time for w in data.works)
    content += f"## Resumo Geral: **{total_h}h** totais\n\n"
    
    # Agrupar por data
    by_date = {}
    for w in data.works:
        by_date.setdefault(w.date, []).append(w)
    
    for d in sorted(by_date.keys(), reverse=True):
        content += f"### 📅 {d} ({sum(x.time for x in by_date[d])}h)\n"
        for w in by_date[d]:
            ref = ""
            if w.idaction:
                a = data.get_action_by_code(w.idaction)
                ref = f"AÇÃO: {a.name}" if a else "Ação Desativada"
            elif w.idissue:
                i = data.get_issue_by_code(w.idissue)
                ref = f"ISSUE: {i.description[:30]}..." if i else "Issue Desativada"
            
            content += f"- **{w.time}h**: {w.description} *({ref})*\n"
        content += "\n"
        
    report_path.write_text(content, encoding='utf-8')
    print(f"[green]Relatório gerado em [bold]{report_path}[/bold][/green]")

def work_mark():
    """Gera o arquivo .project/worklogs.md mantendo tags de trabalho citadas pelo usuário."""
    if not _check_init(): return
    data = ProjectData.load_or_create()
    sync_path = get_db_dir() / 'worklogs.md'
    
    # 1. Extrair tags existentes (> DATA HORA DESCRIÇÃO)
    existing_tags = {} # {ID: [tags]}
    if sync_path.exists():
        txt = sync_path.read_text(encoding='utf-8')
        current_id = None
        for line in txt.split('\n'):
            line_strip = line.strip()
            if not line_strip: continue
            
            # Primeiro verifica se é uma linha de registro de trabalho (tag)
            if line_strip.startswith(">") and current_id:
                # Preservar linha de citação se houver um ID ativo
                # Ignorar a linha de aviso do cabeçalho
                if "Este arquivo contém as ações" not in line:
                    existing_tags.setdefault(current_id, []).append(line)
            else:
                # Só busca ID de referência se não for uma linha de tag
                id_match = re.search(r"<!-- \[(.*?)\] -->", line_strip)
                if id_match:
                    current_id = id_match.group(1)
                elif not line_strip.startswith(">"):
                    # Resetar ID se encontrar outra estrutura que não seja continuação de tag
                    current_id = None

    # 2. Gerar conteúdo
    lines = ["# works do Projeto\n"]
    lines.append("> Este arquivo contém as ações e marcos pendentes para registro de trabalho.\n")
    
    def add_item_with_tags(item_id, text, status_val):
        lines.append(f"- {status_val} {text} <!-- [{item_id}] -->")
        
        # 1. Trazer registros que JÁ ESTÃO no banco para este item
        db_works = [w for w in data.works if (w.idaction == item_id or w.idissue == item_id)]
        for w in sorted(db_works, key=lambda x: x.date):
            lines.append(f"  > {w.date} {w.time} {w.description} <!-- [{w.idwork}] -->")

        # 2. Trazer registros que estão APENAS no arquivo (rascunhos sem ID)
        if item_id in existing_tags:
            for tag in existing_tags[item_id]:
                # Só adiciona se for rascunho (não tem o ID de comentário no final)
                if "<!-- [" not in tag:
                    # Garante indentação de 2 espaços
                    clean_tag = tag.strip()
                    if not clean_tag.startswith("  >"):
                        clean_tag = "  " + clean_tag
                    lines.append(clean_tag)
        
        lines.append("") # Salta uma linha entre cada ação/item

    # Marcos e Ações pendentes
    milestones = [m for m in data.milestones if m.status not in [StatusEnum.CONCLUIDO, StatusEnum.CANCELADO]]
    for m in sorted(milestones, key=lambda x: x.sequence):
        lines.append(f"\n### 🚩 {m.name} ({m.status.value})")
        actions = [a for a in data.actions if a.idmilestone == m.idmilestone and a.status not in [StatusEnum.CONCLUIDO, StatusEnum.CANCELADO]]
        if not actions:
            lines.append("- *Nenhuma ação pendente registrada para este marco.*")
        else:
            for a in sorted(actions, key=lambda x: x.sequence):
                add_item_with_tags(a.idaction, a.name, a.status.value)
            
    # Ações sem marco pendentes
    actions_no_m = [a for a in data.actions if not a.idmilestone and a.status not in [StatusEnum.CONCLUIDO, StatusEnum.CANCELADO]]
    if actions_no_m:
        lines.append("\n### ⚡ Outras Ações (Sem Marco)")
        for a in sorted(actions_no_m, key=lambda x: x.sequence):
            add_item_with_tags(a.idaction, a.name, a.status.value)

    # Issues abertas
    issues = [i for i in data.issues if i.status not in [StatusEnum.CONCLUIDO, StatusEnum.CANCELADO]]
    if issues:
        lines.append("\n### 🐛 Issues Abertas")
        for i in sorted(issues, key=lambda x: x.sequence):
            add_item_with_tags(i.idissues, i.description, i.status.value)

    sync_path.write_text("\n".join(lines) + "\n", encoding='utf-8')
    print(f"[green]Arquivo [bold]worklogs.md[/bold] atualizado com preservação de tags.[/green]")
