from app.project_data import ProjectData, get_db_dir
from app.archive import write_pydantic
from app.issue_md_sync import sync_issues_markdown
from app.action_md_sync import sync_actions_markdown
from pathlib import Path
from rich import print

def read_project_short(file_name='Project Short.md'):
    path_ps = Path(file_name)
    if not path_ps.exists():
        return None
    return path_ps.read_text(encoding='utf-8')

def parse_project_short_text(txt):
    """Extrai nome, descrição e blocos do texto do Project Short.md"""
    blocos = [vl for vl in txt.split('\n\n') if len(vl.strip()) > 0]
    if len(blocos) < 2:
        return None, None, []
    name = blocos[0].replace('# ', '')
    description = blocos[1].replace('> ', '')
    blocos_restantes = blocos[2:]

    return name, description, blocos_restantes

def process_blocos(blocos, data):
    code = 0
    for bloco in blocos:
        tabela = bloco.split('\n')
        linha = tabela[0]
        tabelax = tabela[1:]

        if linha.count('*') == 0:
            for action in tabela:
                if action.strip():
                    data.add_actions(action, None)
        elif linha.count('*') == 1 and linha.upper().count('ISSUES') == 0:
            code += 1
            idmilestone = data.add_milestones(linha.replace('*', ''))
            for action in tabelax:
                if action.strip():
                    data.add_actions(action, idmilestone)
        elif bloco.count('*') == 1 and linha.upper().count('ISSUES') == 1:
            from datetime import date
            today = date.today().isoformat()
            for action in tabelax:
                if action.strip():
                    data.add_issues(action, today)

    return data

def project_init(file_name='Project Short.md'):
    # Verificar se já existe banco de dados
    if (get_db_dir() / 'db.json').exists():
        print("[yellow]Aviso: O projeto já foi inicializado neste diretório.[/yellow]")
        print("Para aplicar mudanças no arquivo Markdown, use: [bold cyan]proj project update[/bold cyan]")
        return False

    path_ps = Path(file_name)
    if not path_ps.exists():
        template = "# Name project\n\n> descrição do project\n\n* marco\nações\nações\nações\n\n* marco\nações\nações\nações\n"
        path_ps.write_text(template, encoding='utf-8')
        print(f"[yellow]Arquivo {file_name} criado automaticamente.[/yellow]")
        print(f"[bold cyan]Por favor, preencha o arquivo '{file_name}' e execute o comando novamente para inicializar o banco.[/bold cyan]")
        return False
    
    txt = read_project_short(file_name)
    name, description, blocos = parse_project_short_text(txt)
    if not name or not description:
        print("[red]Erro: Arquivo Project Short.md está incompleto ou mal formatado.[/red]")
        return False

    data = ProjectData.load_or_create(name, description)
    # No init, se já existir DB, ele apenas adiciona se estiver vazio ou sobrescreve?
    # Para simplificar, se já tem DB, trataremos como um update ou erro.
    # Mas o usuário quer que o init crie o banco a partir do arquivo.
    data.clear_structure() # Garante que começamos do zero a partir do MD
    data = process_blocos(blocos, data)
    write_pydantic(data)
    sync_issues_markdown(import_data=False, data=data)
    sync_actions_markdown(import_data=False, data=data)
    print(f"[green]Projeto '{name}' inicializado com sucesso![/green]")
    return True

def project_update(file_name='Project Short.md'):
    txt = read_project_short(file_name)
    if txt is None:
        print(f"[red]Erro: Arquivo '{file_name}' não encontrado.[/red]")
        return False
    
    name, description, blocos = parse_project_short_text(txt)
    if not name or not description:
        print("[red]Erro: Estrutura do arquivo Project Short.md inválida.[/red]")
        return False

    try:
        data = ProjectData.load_or_create(name, description)
        data.project.name = name
        data.project.description = description
        data.clear_structure()
        data = process_blocos(blocos, data)
        write_pydantic(data)
        sync_issues_markdown(data=data)
        sync_actions_markdown(data=data)
        print(f"[green]Projeto atualizado com sucesso a partir de '{file_name}'![/green]")
        return True
    except Exception as e:
        print(f"[red]Erro ao atualizar projeto: {e}[/red]")
        return False

def main_import_project_short(file_name='Project Short.md'):
    project_init(file_name)

if __name__ == '__main__':
    main_import_project_short()
