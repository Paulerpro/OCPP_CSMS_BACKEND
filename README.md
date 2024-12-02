OCPP Central System Management Software (CSMS)
This project is an OCPP-compliant Central System Management Software (CSMS) built with Django, RabbitMQ, and WebSocket. The project follows a Microservices and Event-Driven Architecture (EDA) to handle the core operations of Electric Vehicle (EV) Charging Points and Charging Station Management.

Project Overview
The CSMS project enables seamless communication between EV Charge Points and a central management system. It supports core OCPP functionalities, including BootNotification, Heartbeat, StartTransaction, StopTransaction, and more, while adhering to modular design principles.

Core Features
OCPP Protocol Compliance: Implements the Open Charge Point Protocol (OCPP) for communication between Charge Points and the CSMS.
Microservices Architecture: Independent services for authentication, charging station management, transaction handling, and notifications.
Event-Driven Design: Real-time message passing using RabbitMQ as the central message broker.
WebSocket Communication: Bi-directional communication between Charge Points and the CSMS.
Scalability: Each service is independently scalable to meet growing demand.
Architecture
The project employs Microservices and Event-Driven Architecture (EDA). Each service is responsible for a specific domain and communicates via RabbitMQ. Here's an overview of the architecture:

Microservices
Authentication Service: Manages user authentication and access control.
Charging Station Service: Maintains Charge Point metadata and handles BootNotification events.
Transaction Service: Tracks charging sessions and manages billing operations.
Notification Service: Sends real-time notifications and alerts.
Charge Point Service (Simulator): Simulates Charge Points for testing the CSMS.
Event-Driven Flow
RabbitMQ acts as the message broker, enabling asynchronous communication between services.
Services publish and subscribe to events such as boot_notification_received, transaction_started, etc.

How It Works

BootNotification:
The Charge Point connects to the CSMS using WebSocket.
Sends a BootNotification payload (e.g., vendor and model details).
CSMS processes and stores the information, then responds with Accepted or Rejected.

Event Handling:
Events are published to RabbitMQ (e.g., boot_notification_received).
Relevant services consume the event and perform corresponding actions.

Real-Time Communication:
WebSockets enable bi-directional communication between Charge Points and the CSMS.

Technologies Used
Backend
Django: Web framework for building each microservice.
Django REST Framework (DRF): For API development.
RabbitMQ: Message broker for asynchronous communication.
WebSocket: Real-time communication between Charge Points and the CSMS.
PostgreSQL: Database for persistent storage.
Libraries
ocpp: Python library for implementing OCPP protocols.
Django Channels: For WebSocket support (optional for real-time use).

Key Endpoints
Authentication Service
POST /login: Authenticate a user.
POST /register: Register a new user.

Charging Station Service
POST /boot-notification: Accept BootNotification payloads.
GET /stations: List registered charging stations.

Transaction Service
POST /start-transaction: Start a charging session.
POST /stop-transaction: Stop a charging session.

Testing and Debugging
Use tools like Postman to test REST APIs for each service.
Monitor RabbitMQ queues and messages via its management console.
Test WebSocket endpoints using libraries like websockets or wscat.

Future Enhancements
Add support for more OCPP messages (e.g., Heartbeat, FirmwareUpdate).
Integrate advanced billing systems for transactions.
Implement a dashboard for monitoring Charge Points in real time.
