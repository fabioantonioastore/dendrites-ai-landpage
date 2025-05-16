from uuid import uuid4


async def uuid4_factory() -> str:
    return str(uuid4())
