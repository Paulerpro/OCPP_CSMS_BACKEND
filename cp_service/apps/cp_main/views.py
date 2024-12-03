import asyncio 

from ocpp.v201.enums import RegistrationStatusType
from ocpp.v201 import call
from ocpp.v201 import ChargePoint as cp

import logging
import websockets

logging.basicConfig(level=logging.INFO)

class ChargePoint(cp):

    """SEND BOOTNOTIFICATION MESSAGE TO THE CENTRAL SYSTEM CONTAINING THE CP's HARDWARE FEATURES"""
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charging_station={
                "model": "Wallbox XYZ", # dynamic?
                "vendor_name": "anewone", # dynamic?
            },
            reason="PowerUp"
        )
        response = await self.call(request)

        if response.status == RegistrationStatusType.accepted:
            print("Connected to CS")

async def main():
    async with websockets.connect(
        "ws://localhost:9000/CP_1",
        subprotocols=["ocpp2.0.1"]
    ) as ws:
        cp = ChargePoint('CP_1', ws)

        await asyncio.gather(cp.start(), cp.send_boot_notification())

asyncio.run(main())