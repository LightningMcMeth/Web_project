from channels.consumer import AsyncConsumer


class YourConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, event):

        textData = event.get('text', None)
        if textData:

            print(f"received from client: {textData}")

            if textData == "ping" or textData == "Ping":
                await self.send({
                    "type": "websocket.send",
                    "text": "pong"})
            else:
                await self.send({
                    "type": "websocket.send",
                    "text": "not pong :("})

    async def websocket_disconnect(self, event):
        print('socket disconnected')
