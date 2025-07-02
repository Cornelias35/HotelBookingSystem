async def notify_clients(sio, data):
    await sio.emit("new_reservation", data)