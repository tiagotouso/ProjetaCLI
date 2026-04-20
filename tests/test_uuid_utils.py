import re
from app.uuid_utils import generate_uuid

def test_generate_uuid_format():
    uuid_str = generate_uuid()
    # UUID4 padrão: 8-4-4-4-12 caracteres hexadecimais
    pattern = r"^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$"
    assert re.match(pattern, uuid_str), f"UUID inválido: {uuid_str}"

def test_generate_uuid_uniqueness():
    uuids = {generate_uuid() for _ in range(1000)}
    assert len(uuids) == 1000, "UUIDs gerados não são únicos"
