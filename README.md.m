
# Collaborative Document Editor (CRDT vs. OT)

This project implements a collaborative document editor prototype with two different conflict resolution algorithms: **CRDT (Conflict-Free Replicated Data Types)** and **OT (Operational Transformation)**. The goal is to showcase how distributed systems can handle concurrent edits in real-time with conflict resolution.

### Algorithms Overview

- **CRDT (Conflict-Free Replicated Data Types)**:
  - CRDTs are designed to allow multiple replicas of data to be updated independently without the need for a central coordinator. It ensures that all changes (insertions, deletions) from multiple clients are merged automatically without conflicts.
  - This prototype uses a **Grow-only Counter (G-Counter)** and a **Replicated Growable Array (RGA)** CRDT for text editing. All operations (insert and delete) are propagated and merged across nodes, ensuring consistency.

- **OT (Operational Transformation)**:
  - OT is a more common technique in collaborative text editing systems (like Google Docs). OT ensures that concurrent operations (such as insertion or deletion of characters) are applied in the correct order.
  - This implementation uses OT to transform operations based on previously applied operations to maintain consistency and ensure the correct order of changes.

---

### How to Run the Project

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bharatnishant/collaborative-editor-flask.git
   cd collaborative-editor
   ```

2. **Build and start the Docker containers**:
   - This will start both the Flask application and Redis server.
   ```bash
   docker-compose up --build
   ```

3. **Access the Flask application**:
   - The app will be available at `http://localhost:8001` for both CRDT and OT endpoints.

---

### Testing the Endpoints

#### CRDT (Conflict-Free Replicated Data Type)

- **Insert a character**:
  ```bash
  curl -X POST http://localhost:8001/crdt -H "Content-Type: application/json" -d '{"type": "insert", "position": 0, "char": "H", "client_id": "1"}'
  ```

- **Get current document content**:
  ```bash
  curl -X GET http://localhost:8001/crdt
  ```

- **Delete a character**:
  ```bash
  curl -X POST http://localhost:8001/crdt -H "Content-Type: application/json" -d '{"type": "delete", "position": 0, "client_id": "1"}'
  ```

#### OT (Operational Transformation)

- **Insert a character**:
  ```bash
  curl -X POST http://localhost:8001/ot -H "Content-Type: application/json" -d '{"type": "insert", "position": 0, "char": "A", "client_id": "2"}'
  ```

- **Get current document content**:
  ```bash
  curl -X GET http://localhost:8001/ot
  ```

- **Delete a character**:
  ```bash
  curl -X POST http://localhost:8001/ot -H "Content-Type: application/json" -d '{"type": "delete", "position": 0, "client_id": "2"}'
  ```

---

### Project Structure

```plaintext
collaborative_editor/
├── app/
│   ├── crdt.py                 # CRDT logic
│   ├── ot.py                   # OT logic
│   ├── app.py                  # Flask application
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # Dockerfile for Flask app
│   ├── redis_config.py         # Redis configuration
├── docker-compose.yml          # Docker Compose file
└── README.md                   # Instructions
```

---

### Technologies Used

- **Flask**: Python web framework for the backend API.
- **Redis**: In-memory data store for shared state and synchronization.
- **Docker**: Containerization for simulating multiple nodes.
- **JSON**: Format for storing and transmitting operations.

---