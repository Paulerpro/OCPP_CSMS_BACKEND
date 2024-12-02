import asyncio
import logging
import websockets
from datetime import datetime

from ocpp.routing import on
from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call_result
from ocpp.v201.enums import RegistrationStatusType

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):

    '''FUNCTION TO LISTEN AND CONSTRUCT RESPONSE FOR BOOTNOTIFICATION EVENTS'''
    # Decorator enables the async func (on_boot_notification)...
    # listens and processes BOOTNOFITICATION Event from the charging station (i.e Event Listener)
    @on('BootNotification') 
    async def on_boot_notification(self, charging_station, reason, **kwargs):
        return call_result.BootNotificationPayload(
            current_time=datetime.now().isoformat, # timestamp to inform CS time of notification procession
            interval=10, # duration until further updates from CS
            status=RegistrationStatusType.accepted #e enum status that CSMS registration is accepted
        )

async def on_connect(websocket, path):
    """ For every new charge point that connects, 
    create a ChargePoint instance and start listening for messages.
    """
    try:
        # Extract the Sec-WebSocket-Protocol header from the WebSocket request if any.
        requested_protocols = websocket.request_headers[
            'Sec-WebSocket-Protocol'
        ]
    except KeyError:
        # handle error and close connect if not required header
        logging.info("Client hasn't requested any Subprotocol. "
                        "Closing Connection"
                        )
        return await websocket.close()

    # Checks if WebSocket connection has a negotiated subprotocol.
    if websocket.subprotocol:
        logging.info("Protocols Matchwed: %s", websocket.subprotocol)
    else:
        # In the websockets lib if no subprotocols are supported by the
        # client and the server, it proceeds without a subprotocol,
        # so we have to manually close the connection.
        logging.warning('Protocols Mismatched | Expected Subprotocol: %s,'
                        ' but cliet supports %s | Closing connection',
                        websocket.available_subprotocols,
                        requested_protocols)
        return await websocket.close()
    
    # get CP's id fom websocket path and create CP instance
    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)

    # start listening & processing incoming messages from the connected CP
    await cp.start()

async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp2.0.1']
    )

    logging.info('Websocket Server Started')
    await server.wait_closed()

asyncio.run(main())
