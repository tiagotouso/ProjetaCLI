import uuid

def generate_uuid() -> str:
    """
    Gera um UUID4 único como string.
    """
    return str(uuid.uuid4())
