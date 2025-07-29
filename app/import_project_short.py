from app.project_data import ProjectData
from pathlib import Path
from rich import print


def read_project_short():

    path_ps = Path('Project Short.md')
    return path_ps.read_text(encoding='utf-8')


if __name__ == '__main__':


    data = None
    txt = read_project_short()

    code = '1'
    name, description = '', ''

    blocos = [vl for vl in txt.split('\n\n') if len(vl.strip()) > 0]

    name = blocos[0].replace('# ', '')
    description = blocos[1].replace('> ', '')
    blocos = blocos[2:]

    data = ProjectData.load_or_create('1', name, description)

    code = 0
    for bloco in blocos:
        tabela = bloco.split('\n')
        linha = tabela[0]
        tabelax = tabela[1:]

        if linha.count('*') == 0:
            for action in tabela:
                data.add_actions(action)
        elif linha.count('*') == 1 and linha.upper().count('ISSUES') == 0:
            code += 1
            data.add_milestones(linha.replace('*', ''))
            for action in tabelax:
                data.add_actions(action, str(code))
        elif bloco.count('*') == 1 and linha.upper().count('ISSUES') == 1:
            data.add_issues(action)

    # gravar_modelo_em_json(data)


    print(data)

