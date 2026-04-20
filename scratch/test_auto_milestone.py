from app.project_data import ProjectData
from app.models import StatusEnum

data = ProjectData.load_or_create()

# 1. Criar uma milestone de teste
m_id = data.add_milestones("Teste Auto Conclusão")
# 2. Criar uma ação vinculada
data.add_actions("Ação de Teste", m_id)

# 3. Salvar (milestone deve estar AGUARDANDO)
data.save()
m = data.get_melistones_by_code(m_id)
print(f"Status Inicial da Milestone: {m.status.value}")

# 4. Marcar ação como concluída
action = [a for a in data.actions if a.idmilestone == m_id][0]
action.status = StatusEnum.CONCLUIDO
data.needs_sync = True # Simula o que o console faria

# 5. Salvar (deve disparar a sincronização)
data.save()
m = data.get_melistones_by_code(m_id)
print(f"Status Final da Milestone: {m.status.value}")

if m.status == StatusEnum.CONCLUIDO:
    print("Sucesso: Milestone concluída automaticamente!")
else:
    print("Falha: Milestone não foi concluída.")
