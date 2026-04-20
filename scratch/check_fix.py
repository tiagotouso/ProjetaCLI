from app.project_data import ProjectData
from app.models import StatusEnum

# Forçamos uma situação onde uma ação está concluída mas a milestone não
data = ProjectData.load_or_create()

# Vamos garantir que temos uma milestone e ações vinculadas
m_id = data.add_milestones("Teste Bug Correcao")
data.add_actions("Açao 1", m_id)
data.add_actions("Açao 2", m_id)

# Salva estado inicial
data.save()

# Agora marcamos ambas as ações como concluídas e setamos needs_sync
# Simulando a operação feita pelo console que acabamos de corrigir
for a in data.actions:
    if a.idmilestone == m_id:
        a.status = StatusEnum.CONCLUIDO

data.needs_sync = True
data.save() # Aqui deve ocorrer a mágica e a milestone deve virar CONCLUIDO

m = data.get_melistones_by_code(m_id)
print(f"Milestone '{m.name}' status: {m.status.value}")

if m.status == StatusEnum.CONCLUIDO:
    print("Sucesso: A milestone foi atualizada corretamente!")
else:
    print("Erro: A milestone ainda não está concluída.")
