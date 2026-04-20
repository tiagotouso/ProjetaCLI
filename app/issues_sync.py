from app.issue_md_sync import sync_issues_markdown

def sync_issues():
    """Wrapper para manter o comando CLI funcionando direcionado ao Markdown."""
    sync_issues_markdown()
