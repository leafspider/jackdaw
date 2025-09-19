import json

def jwrap(name, content):
    return json.dumps({"name": name, "content": content})

async def send(websocket, name, para):
    if websocket != None:
        return await websocket.send(jwrap(name,para))
    else:
        return None
