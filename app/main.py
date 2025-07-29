
# import typer
# from rich import print
from app.archive import write_pydantic

# app = typer.Typer(help="A CLI for managing projects.")

# # @app.command()
# # def add(
# #     name: str = typer.Option(..., "--name", "-n", help="The name of the project."),
# #     description: str = typer.Option(..., "--description", "-d", help="The description of the project."),
# # ):
# #     """Adds a new project to the database."""
# #     db = ProjectDB()
# #     project_code = db.project_insert(name, description)
# #     db.close()
# #     if project_code:
# #         print(f"Project '{name}' added with code: {project_code}")
# #     else:
# #         print(f"Failed to add project '{name}'. It might already exist.")


# @app.command()
# def add(
#     name: str = typer.Argument(..., help="The name of the project."),
#     description: str = typer.Argument(..., help="The description of the project."),
#     verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output.")
# ):
#     """Adds a new project to the database."""
#     db = ProjectDB()
#     project_code = db.project_insert(name, description)
#     db.close()
#     if project_code:
#         if verbose:
#             print(f"Project '{name}' added with code: {project_code}")
#         else:
#             print(f"Project added with code: {project_code}")
#     else:
#         print(f"Failed to add project '{name}'. It might already exist.")

# # python main.py add "Meu Projeto" "Descrição do projeto" --verbose

# @app.command()
# def select():
#     project_db = ProjectDB()
#     project = project_db.project_select()
#     print(project)



# if __name__ == "__main__":
#     app()

from pathlib import Path
from rich import print
from app.project_data import ProjectData


def main():
    print('-' * 80)
    print(Path('.').absolute())
    print('-' * 80)

    data = ProjectData.load_or_create('1', 'teste', 'teste')
    print(data)
    write_pydantic(data)



if __name__ == '__main__':
    main()
