# Ghost Shell OS - API Reference

## Overview

Ghost Shell provides a RESTful API through its WebServer engine, enabling remote system control, monitoring, and automation. The API follows standard HTTP conventions with JSON request/response bodies.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All API requests require authentication via session token:

```
Authorization: Bearer <session_token>
Content-Type: application/json
```

## Response Format

All responses follow this standard structure:

```json
{
  "status": "success|error",
  "data": { /* response data */ },
  "message": "Human-readable message",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created
- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Endpoints

### Authentication

#### POST /auth/login
Authenticate and receive session token.

**Request:**
```json
{
  "username": "admin",
  "password": "secure_password"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 3600,
    "user": {
      "id": "user_123",
      "username": "admin",
      "roles": ["admin", "operator"]
    }
  }
}
```

#### POST /auth/logout
Revoke session token.

**Response:**
```json
{
  "status": "success",
  "message": "Logged out successfully"
}
```

### System Information

#### GET /system/info
Get comprehensive system information.

**Response:**
```json
{
  "status": "success",
  "data": {
    "hostname": "ghost-shell-01",
    "os": "Windows",
    "platform": "win32",
    "uptime_seconds": 86400,
    "version": "v6.0-Ghost-Kernel",
    "python_version": "3.9.2",
    "memory": {
      "total_mb": 8192,
      "available_mb": 4096
    },
    "disk": {
      "total_gb": 500,
      "free_gb": 250
    }
  }
}
```

#### GET /system/status
Get system health and component status.

**Response:**
```json
{
  "status": "success",
  "data": {
    "health": "healthy",
    "engines": {
      "ghost_core": "running",
      "security": "running",
      "heartbeat": "running",
      "reminder": "running",
      "vault": "ready",
      "webserver": "listening"
    },
    "services": {
      "reminder_pulse": "active",
      "heartbeat_monitor": "active"
    },
    "alerts": []
  }
}
```

### Engine Management

#### GET /engines
List all engines with status.

**Response:**
```json
{
  "status": "success",
  "data": {
    "engines": [
      {
        "name": "ghost_core",
        "display_name": "The GhostCoreEngine",
        "emoji": "👻",
        "status": "running",
        "uptime_ms": 3600000,
        "version": "1.0.0"
      }
    ],
    "total_count": 11
  }
}
```

#### GET /engines/{engine_name}
Get specific engine details.

**Response:**
```json
{
  "status": "success",
  "data": {
    "name": "security",
    "display_name": "The SecurityEngine",
    "description": "Gatekeeper for system access",
    "status": "running",
    "methods": ["authenticate", "authorize", "validate_token"],
    "metrics": {
      "requests_handled": 2341,
      "auth_failures": 3,
      "vault_operations": 156
    }
  }
}
```

#### POST /engines/{engine_name}/restart
Restart a specific engine.

**Response:**
```json
{
  "status": "success",
  "message": "Engine restarted successfully",
  "data": {
    "engine": "reminder",
    "restart_time_ms": 245
  }
}
```

### Reminders

#### GET /reminders
List all scheduled reminders.

**Query Parameters:**
- `status` - Filter by status: `pending`, `active`, `completed`
- `limit` - Max results (default: 50)
- `offset` - Pagination offset (default: 0)

**Response:**
```json
{
  "status": "success",
  "data": {
    "reminders": [
      {
        "id": "rem_123",
        "message": "Check system backup",
        "due_time": "2024-01-15T14:30:00Z",
        "frequency": "daily",
        "status": "active",
        "created_at": "2024-01-10T10:00:00Z"
      }
    ],
    "total_count": 42,
    "limit": 50,
    "offset": 0
  }
}
```

#### POST /reminders
Create new reminder.

**Request:**
```json
{
  "message": "Update security patches",
  "due_time": "2024-01-16T10:00:00Z",
  "frequency": "weekly",
  "notification_channels": ["email", "in_app"]
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "id": "rem_456",
    "message": "Update security patches",
    "due_time": "2024-01-16T10:00:00Z",
    "frequency": "weekly",
    "status": "pending",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### DELETE /reminders/{reminder_id}
Delete reminder.

**Response:**
```json
{
  "status": "success",
  "message": "Reminder deleted"
}
```

### Commands

#### GET /commands
List available commands.

**Response:**
```json
{
  "status": "success",
  "data": {
    "commands": [
      {
        "name": "shell",
        "description": "Launch interactive shell",
        "status": "Phase 1 COMPLETE",
        "arguments": []
      },
      {
        "name": "remind",
        "description": "Schedule reminders",
        "status": "Phase 1 COMPLETE",
        "arguments": ["message", "due_time", "frequency"]
      }
    ],
    "total_count": 25
  }
}
```

#### POST /commands/execute
Execute a command via API.

**Request:**
```json
{
  "command": "status",
  "arguments": []
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "command_result": "System operational. All engines running.",
    "execution_time_ms": 145
  }
}
```

### Vault/Security

#### POST /vault/encrypt
Encrypt sensitive data.

**Request:**
```json
{
  "plaintext": "secret_password_123"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "ciphertext": "AES_ENCRYPTED_DATA_HEX...",
    "algorithm": "AES-256-GCM",
    "iv": "INITIALIZATION_VECTOR_HEX"
  }
}
```

#### POST /vault/decrypt
Decrypt sensitive data.

**Request:**
```json
{
  "ciphertext": "AES_ENCRYPTED_DATA_HEX...",
  "iv": "INITIALIZATION_VECTOR_HEX"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "plaintext": "secret_password_123"
  }
}
```

#### GET /vault/keys
List encrypted keys in vault.

**Response:**
```json
{
  "status": "success",
  "data": {
    "keys": [
      {
        "id": "key_001",
        "name": "admin_password",
        "created_at": "2024-01-10T10:00:00Z",
        "last_used": "2024-01-15T09:30:00Z"
      }
    ],
    "total_count": 12
  }
}
```

### Host Bridge

#### GET /hosts
Discover and list available hosts.

**Response:**
```json
{
  "status": "success",
  "data": {
    "hosts": [
      {
        "id": "host_001",
        "hostname": "workstation-01",
        "ip_address": "192.168.1.100",
        "status": "online",
        "last_seen": "2024-01-15T10:25:00Z",
        "services": ["webserver", "database"]
      }
    ],
    "total_count": 3
  }
}
```

#### POST /hosts/{host_id}/execute
Execute command on remote host.

**Request:**
```json
{
  "command": "dir C:\\",
  "timeout_seconds": 30
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "stdout": "Volume in drive C is SYSTEM...",
    "stderr": "",
    "exit_code": 0,
    "execution_time_ms": 245
  }
}
```

## Error Handling

API errors return consistent error structure:

```json
{
  "status": "error",
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "Missing required parameter: message",
    "details": {
      "parameter": "message",
      "expected_type": "string"
    }
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Rate Limiting

- Rate limit: 1000 requests per minute
- Headers returned:
  - `X-RateLimit-Limit: 1000`
  - `X-RateLimit-Remaining: 999`
  - `X-RateLimit-Reset: 1705319460`

## WebSocket Events

Ghost Shell supports WebSocket connections for real-time updates:

```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/events');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Handle engine status updates, reminders, etc.
};
```

Event types:
- `engine.status_change` - Engine status changed
- `reminder.triggered` - Reminder activated
- `system.alert` - System alert
- `command.completed` - Command execution finished

## SDK/Client Libraries

### Python
```python
from ghostshell import GhostShellClient

client = GhostShellClient(
    base_url='http://localhost:8000',
    username='admin',
    password='password'
)

status = client.system.get_status()
reminders = client.reminders.list(limit=10)
```

### JavaScript/Node.js
```javascript
const GhostShell = require('ghostshell-api');

const client = new GhostShell({
  baseURL: 'http://localhost:8000',
  token: 'your_session_token'
});

await client.system.getStatus();
await client.reminders.list({ limit: 10 });
```
