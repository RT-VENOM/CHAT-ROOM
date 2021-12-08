import asyncio
import threading
import websockets
import os 

from websockets.server import ServerConnection
clients = []
nicknames = []
casting = []
casting_nick = []
connection = ServerConnection()




async def recieve(websocket):

        
    async def all(message):
        for client in clients:
            await client.send(message)
    ip = websocket.remote_address[0]
    print(f'Connected with {str(ip)}')
    await websocket.send("NICK")
    name = await websocket.recv()
    nicknames.append(name)
    clients.append(websocket)
    print(f'Nickname of the client is {name}')
    await websocket.send('Connected to the server!')
    await all(f'{name} joined the chat!')
    while True:
        try:
            data= await websocket.recv()
            if data == "list()":
                await websocket.send(", ".join(nicknames))
            else:
                await all(data)
        except:
            index = clients.index(websocket)
            clients.remove(websocket)
            nick = nicknames[index]
            await all(f"{nick} left the chat!")
            nicknames.remove(nick)
            break
        






async def main():
    async with websockets.serve(recieve, "0.0.0.0", os.getenv('PORT')):
        print("Server is listening!")
        await asyncio.Future()  # run forever


asyncio.run(main())
