# 🎯 ProjetaCLI

> Uma interface de linha de comando (CLI) elegante e eficiente para gerenciamento ágil de projetos, focada na simplicidade e produtividade diretamente do terminal.

O **ProjetaCLI** permite que você planeje, execute e acompanhe o ciclo de vida dos seus projetos através de uma interface interativa, mantendo um registro claro de marcos, tarefas e logs de trabalho.

---

## ✨ Funcionalidades

- **📁 Gerenciamento de Projetos**: Criação e visualização detalhada do status global do projeto.
- **🚩 Marcos (Milestones)**: Organize seu progresso em fases lógicas e entregáveis.
- **⚡ Ações (Actions)**: Controle granular de tarefas com atualizações de status em tempo real.
- **⚠️ Issues**: Registro e acompanhamento de problemas ou impedimentos encontrados.
- **⏱️ WorkLog**: Apontamento de horas e descrição das atividades realizadas em cada ação.
- **📝 Importação Inteligente**: Converta rascunhos markdown (`Project Short.md`) em dados estruturados automaticamente.
- **📊 Relatórios Automatizados**: Geração de relatórios completos em Markdown (`Project Report.md`) para acompanhamento de stakeholders.

---

## 🛠️ Tecnologias

Este projeto utiliza ferramentas modernas do ecossistema Python para garantir performance e uma excelente experiência de usuário:

- **[Python 3.12+](https://www.python.org/)**: Linguagem base.
- **[Typer](https://typer.tiangolo.com/)**: Para a estrutura robusta de comandos e subcomandos.
- **[InquirerPy](https://inquirerpy.readthedocs.io/)**: Fornece menus interativos e seleções intuitivas no terminal.
- **[Pydantic V2](https://docs.pydantic.dev/)**: Para modelagem de dados rigorosa e serialização JSON.
- **[Rich](https://rich.readthedocs.io/)**: Para saídas de terminal visualmente ricas com tabelas e cores.
- **[UV](https://github.com/astral-sh/uv)**: Gerenciador de dependências extremamente rápido.

---

## 🚀 Como Começar

### Instalação

1. Certifique-se de ter o `uv` instalado em sua máquina.
2. Clone o repositório:
   ```bash
   git clone https://github.com/tiagotouso/ProjetaCLI.git
   cd ProjetaCLI
   ```
3. Instale as dependências e o ambiente virtual:
   ```bash
   uv sync
   ```

### 💻 Instalando no Console (Global)

Para poder executar o comando `proj` de qualquer lugar no seu terminal, use:
```bash
uv tool install --editable .
```
*(O modo `--editable` permite que mudanças no código reflitam instantaneamente no comando global).*

Se não estiver usando o `uv`, você pode instalar via pip:
```bash
pip install -e .
```

---

## 📖 Guia de Comandos (CLI Help)

O **ProjetaCLI** pode ser operado de duas formas: através de comandos diretos ou via interface interativa.

### 🎫 Comandos Diretos (`proj`)
Execute estes comandos para acesso rápido a informações:

| Comando | Descrição |
| :--- | :--- |
| `proj project show` | Exibe o status geral do projeto, marcos e ações pendentes. |
| `proj works show` | Visualiza o resumo dos registros de trabalho (Worklogs). |
| `proj --help` | Exibe a ajuda geral da CLI. |

### 🕹️ Interface Interativa (Menu Completo)
Para operações de escrita e gerenciamento detalhado, utilize o menu interativo:
```bash
# Se instalado globalmente
python -m app.actions

# Ou via script direto
python app/actions.py
```

Dentro do menu, você encontrará as seguintes opções:

*   **📁 Project**: Visualizar resumo, editar metadados ou gerar o **Relatório Final (`Project Report.md`)**.
*   **🚩 Milestones**: Gerenciar as grandes entregas e fases do projeto.
*   **⚡ Actions**: Criar tarefas, excluir ou **atualizar o status** (Aguardando, Iniciado, Concluído).
*   **⚠️ Issues**: Registrar e acompanhar problemas ou bloqueios.
*   **⏱️ Works**: Apontar horas e descrever o trabalho realizado em cada ação específica.

### 📥 Utilitário de Importação
Para converter um planejamento rápido no formato Markdown para o sistema:
```bash
python -m app.import_project_short
```
*Este comando lê o arquivo `Project Short.md` e popula o banco de dados local automaticamente.*

---

### Executando Testes

O projeto utiliza `pytest` para garantir a qualidade do código:
```bash
$env:PYTHONPATH="."; .venv\Scripts\python.exe -m pytest
```

---

## 📂 Estrutura do Projeto

```text
ProjetaCLI/
├── app/                # Código fonte da aplicação
│   ├── main.py         # Ponto de entrada da CLI (Typer)
│   ├── actions.py      # Lógica do Menu Interativo (InquirerPy)
│   ├── project_data.py # Manipulação e persistência de dados
│   ├── models.py       # Modelos Pydantic (Project, Action, etc)
│   └── ...
├── .project/           # Banco de dados local (JSON)
├── tests/              # Testes unitários e de integração
└── Project Short.md    # Arquivo de entrada para planejamento rápido
```

---

## 📝 Exemplo de Planejamento (`Project Short.md`)

O ProjetaCLI lê arquivos markdown com a seguinte estrutura:

```markdown
# Nome do Projeto
> Descrição do projeto

* Setup Inicial
Inicia o repositório Git localmente
Cria a estrutura de pastas
```

---
Desenvolvido por **Tiago Touso** 🚀
