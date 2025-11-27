# API Documentation

## Base URL
`http://localhost:5000/api`

## Authentication

All endpoints except public API require authentication via session cookies or JWT.

### Authentication Endpoints

#### POST /auth/signup
Register a new user
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secure123",
  "phone": "9999999999",
  "role": "CITIZEN"  // ADMIN, VOLUNTEER, or CITIZEN
}
```

Response:
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "citizen",
    "created_at": "2024-01-15T10:30:00"
  }
}
```

#### POST /auth/login
Login user
```json
{
  "email": "john@example.com",
  "password": "secure123"
}
```

Response:
```json
{
  "message": "Login successful",
  "user": { ... }
}
```

#### POST /auth/logout
Logout current user (requires authentication)

#### GET /auth/me
Get current user info (requires authentication)

---

## Admin API

All admin endpoints require `role=admin`

### GET /admin/dashboard
Get dashboard statistics
```json
{
  "total_reports": 25,
  "pending_reports": 5,
  "active_volunteers": 12,
  "total_resources": 45
}
```

### GET /admin/reports
Get all disaster reports
```
Query params:
- page: int (default: 1)
- per_page: int (default: 10)
- status: string (pending, acknowledged, in_progress, resolved)
```

Response:
```json
{
  "reports": [ ... ],
  "total": 25,
  "pages": 3,
  "current_page": 1
}
```

### GET /admin/reports/<id>
Get specific report with volunteer tasks

### PATCH /admin/reports/<id>/status
Update report status
```json
{
  "status": "in_progress"
}
```

### POST /admin/reports/<id>/assign
Assign volunteer to report
```json
{
  "volunteer_id": 5,
  "task_description": "Provide medical assistance"
}
```

### GET /admin/volunteers
Get all volunteers

### GET /admin/resources
Get all resources

### POST /admin/resources
Create new resource
```json
{
  "name": "First Aid Kit",
  "resource_type": "medical",
  "quantity": 50,
  "unit": "units",
  "location": "City Hospital",
  "contact_person": "Dr. Smith",
  "contact_phone": "9999999999"
}
```

### PATCH /admin/resources/<id>
Update resource

### DELETE /admin/resources/<id>
Delete resource

### GET /admin/alerts
Get all alerts

### POST /admin/alerts
Create and broadcast alert
```json
{
  "title": "Flood Warning",
  "message": "Flash flood expected in downtown area",
  "alert_level": "critical",
  "report_id": 10,
  "is_broadcast": true
}
```

---

## Citizen API

All citizen endpoints require `role=citizen` or any authenticated user

### GET /citizen/dashboard
Get citizen dashboard with their reports, active disasters, and alerts

### GET /citizen/reports
Get citizen's own reports

### POST /citizen/reports
Submit new disaster report
```json
{
  "title": "Building Fire",
  "description": "5-story building on fire, 10 people trapped",
  "location": "Downtown Market Street",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "severity": "CRITICAL",
  "image_url": "https://..."
}
```

### GET /citizen/reports/<id>
Get specific report (must be owner)

### PATCH /citizen/reports/<id>
Update own report

### GET /citizen/reports/<id>/status
Track report status

### GET /citizen/alerts
Get broadcast alerts

---

## Volunteer API

All volunteer endpoints require `role=volunteer`

### GET /volunteer/dashboard
Get volunteer dashboard with task statistics

### GET /volunteer/tasks
Get all assigned tasks
```
Query params:
- status: string (assigned, in_progress, completed, failed)
```

### GET /volunteer/tasks/<id>
Get specific task details

### PATCH /volunteer/tasks/<id>
Update task (status, notes)
```json
{
  "status": "in_progress",
  "notes": "Started rescue operations"
}
```

### POST /volunteer/tasks/<id>/start
Mark task as in progress

### POST /volunteer/tasks/<id>/complete
Mark task as completed

---

## Public API

No authentication required

### GET /public/disasters
Get active/ongoing disaster reports

### GET /public/alerts
Get broadcast alerts
```
Query params:
- limit: int (default: 20)
```

### GET /public/resources
Get available resources
```
Query params:
- type: string (filter by resource type)
```

### GET /public/statistics
Get system statistics
```json
{
  "disaster_stats": {
    "total_reports": 100,
    "active_reports": 15,
    "resolved_reports": 80
  },
  "resource_stats": {
    "total": 500,
    "available": 350
  }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Missing required fields"
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid email or password"
}
```

### 403 Forbidden
```json
{
  "error": "Admin access required"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Status Codes

- `200` - OK
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict (e.g., email already exists)
- `500` - Internal Server Error

---

## Rate Limiting

Currently not implemented. Will be added in production.

## CORS

CORS is enabled for all `/api/*` endpoints. Add frontend domain to allowed origins in `.env` for production.

---

For more information, see the main README.md file.
