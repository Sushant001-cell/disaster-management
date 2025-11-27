# Disaster Management System

A comprehensive real-time disaster management and emergency response platform with role-based access (Admin, Volunteer, Citizen).

## Features

✅ **User Management**
- Role-based authentication (Admin, Volunteer, Citizen)
- Secure password hashing with Werkzeug
- User profiles and location tracking

✅ **Disaster Reporting**
- Citizens can submit disaster reports with location, severity, and description
- Real-time status tracking
- Image/media support

✅ **Volunteer Management**
- Task assignment to volunteers
- Task status tracking (Assigned, In Progress, Completed)
- Volunteer dashboard and workload management

✅ **Resource Management**
- Track emergency resources (medical, shelter, food, transport, etc.)
- Resource availability management
- Contact information for resources

✅ **Alert System**
- Real-time alerts and notifications
- Broadcast alerts to specific roles
- Critical alert management

✅ **Admin Dashboard**
- System statistics and overview
- Report management and updates
- Volunteer assignment and tracking
- Resource management
- Alert broadcasting

✅ **Citizen Dashboard**
- Report disaster incidents
- Track report status
- Receive alerts
- View active disasters

✅ **Volunteer Dashboard**
- View assigned tasks
- Update task progress
- Track completion status
- Workload management

## Tech Stack

**Backend:**
- Flask 3.0
- Flask-SQLAlchemy 3.1 (ORM)
- Flask-Login 0.6 (Authentication)
- Flask-CORS 4.0 (Cross-origin)
- Flask-SocketIO 5.3 (Real-time)
- Werkzeug 3.1 (Security)
- Python-dotenv (Config)

**Frontend:**
- HTML5 / CSS3 / JavaScript (ES6+)
- Leaflet.js (Maps)
- Responsive Design

**Database:**
- SQLite (Development)
- PostgreSQL (Production Ready)

**Deployment:**
- Gunicorn (WSGI Server)
- Eventlet (Async Worker)

## Project Structure

```
disaster-management/
├── backend/
│   ├── app.py              # Main Flask app
│   ├── models.py           # SQLAlchemy models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py         # Login/Signup
│   │   ├── admin.py        # Admin endpoints
│   │   ├── citizen.py      # Citizen endpoints
│   │   ├── volunteer.py    # Volunteer endpoints
│   │   └── api.py          # Public API
│   └── __pycache__/
├── frontend/
│   ├── index.html
│   ├── js/
│   │   └── main.js
│   └── css/
│       └── style.css
├── database/
├── requirements.txt
├── wsgi.py                 # Production entry point
├── .env                    # Environment variables
└── README.md
```

## Installation

### 1. Clone & Setup

```bash
cd disaster-management
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Edit `.env`:
```
FLASK_APP=backend/app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database/disaster.db
```

### 4. Initialize Database

```bash
python
>>> from backend.app import app, db
>>> from backend.models import init_db
>>> init_db(app)
>>> exit()
```

### 5. Create Sample Admin User

```bash
python
>>> from backend.app import app, db
>>> from backend.models import User, UserRole
>>> app.app_context().push()
>>> admin = User(name='Admin', email='admin@disaster.com', role=UserRole.ADMIN)
>>> admin.set_password('admin123')
>>> db.session.add(admin)
>>> db.session.commit()
>>> print("Admin created!")
>>> exit()
```

## Running the Application

### Development Mode

```bash
python backend/app.py
```

Server runs on: `http://localhost:5000`

### Production Mode (with Gunicorn)

```bash
# Windows
python -m gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 wsgi:app

# Linux/Mac
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 wsgi:app
```

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

### Admin Routes
- `GET /api/admin/dashboard` - Dashboard stats
- `GET /api/admin/reports` - All reports
- `GET /api/admin/reports/<id>` - Report details
- `PATCH /api/admin/reports/<id>/status` - Update status
- `POST /api/admin/reports/<id>/assign` - Assign volunteer
- `GET /api/admin/volunteers` - All volunteers
- `GET/POST /api/admin/resources` - Resource management
- `GET/POST /api/admin/alerts` - Alert management

### Citizen Routes
- `GET /api/citizen/dashboard` - Citizen dashboard
- `GET/POST /api/citizen/reports` - Citizen's reports
- `GET/PATCH /api/citizen/reports/<id>` - Manage report
- `GET /api/citizen/reports/<id>/status` - Report status
- `GET /api/citizen/alerts` - Receive alerts

### Volunteer Routes
- `GET /api/volunteer/dashboard` - Task dashboard
- `GET /api/volunteer/tasks` - All assigned tasks
- `GET/PATCH /api/volunteer/tasks/<id>` - Manage task
- `POST /api/volunteer/tasks/<id>/start` - Start task
- `POST /api/volunteer/tasks/<id>/complete` - Complete task

### Public API
- `GET /api/public/disasters` - Active disasters (public)
- `GET /api/public/alerts` - Public alerts
- `GET /api/public/resources` - Available resources
- `GET /api/public/statistics` - System statistics

## Database Models

### User
```
- id, name, email, password_hash, phone, location
- role (admin/volunteer/citizen)
- is_active, created_at, updated_at
```

### DisasterReport
```
- id, title, description, location, lat/lng
- severity (low/medium/high/critical)
- status (pending/acknowledged/in_progress/resolved)
- reporter_id, image_url
- created_at, updated_at, resolved_at
```

### VolunteerTask
```
- id, volunteer_id, report_id, task_description
- status (assigned/in_progress/completed/failed)
- assigned_at, started_at, completed_at, notes
```

### Resource
```
- id, name, resource_type, quantity, unit
- location, availability, contact_person, contact_phone
- created_at, updated_at
```

### Alert
```
- id, title, message, alert_level (info/warning/critical)
- report_id, target_role, is_broadcast
- created_at
```

## Testing the System

### 1. Create Users
- Admin: `admin@disaster.com / admin123`
- Volunteer: `volunteer@disaster.com / vol123`
- Citizen: `citizen@disaster.com / citizen123`

### 2. Test Admin Flow
- Login as admin
- View dashboard stats
- Create resources
- Send alerts

### 3. Test Citizen Flow
- Login as citizen
- Submit disaster report
- Track report status
- Receive alerts

### 4. Test Volunteer Flow
- Login as volunteer
- View assigned tasks
- Update task progress
- Mark completion

## Deployment

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_ENV=production
EXPOSE 5000
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:5000", "wsgi:app"]
```

### AWS EC2
```bash
# Install Python & dependencies
sudo apt-get update
sudo apt-get install python3-pip python3-venv

# Deploy
git clone <repo>
cd disaster-management
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with systemd
sudo systemctl start disaster-management
```

### Heroku
```bash
heroku create disaster-management
git push heroku main
heroku config:set SECRET_KEY=your-secret
```

## Future Enhancements

- [ ] Real-time map updates with Socket.IO
- [ ] SMS/Email notifications
- [ ] Mobile app (React Native)
- [ ] Machine learning for disaster prediction
- [ ] Weather integration
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] File uploads and media management
- [ ] Social media integration
- [ ] AI chatbot for quick assistance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open a Pull Request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for disaster management and emergency response**
