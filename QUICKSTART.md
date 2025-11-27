# 🚀 DISASTER MANAGEMENT SYSTEM - QUICK START GUIDE

## Project Overview

Complete, production-ready disaster management and emergency response platform with:
- ✅ Role-based authentication (Admin, Volunteer, Citizen)
- ✅ Real-time disaster reporting and tracking
- ✅ Volunteer task management
- ✅ Resource management
- ✅ Real-time alerts
- ✅ Modern responsive frontend
- ✅ REST API with Socket.IO

**Built with:** Flask, SQLAlchemy, Flask-Login, Flask-SocketIO, Gunicorn

---

## 📁 Project Structure

```
disaster-management/
├── backend/
│   ├── app.py                    # Flask app factory
│   ├── models.py                 # SQLAlchemy models (User, DisasterReport, etc.)
│   ├── routes/
│   │   ├── __init__.py           # Routes initialization
│   │   ├── auth.py               # Signup/Login/Logout
│   │   ├── admin.py              # Admin endpoints
│   │   ├── citizen.py            # Citizen endpoints
│   │   ├── volunteer.py          # Volunteer endpoints
│   │   └── api.py                # Public API
│   └── __init__.py
├── frontend/
│   ├── index.html                # Single-page app
│   ├── js/main.js                # Frontend logic
│   └── css/style.css             # Responsive styling
├── database/                      # SQLite DB location
├── requirements.txt              # Python dependencies
├── .env                          # Environment configuration
├── wsgi.py                       # Production entry point
├── setup.bat                     # Windows setup script
├── setup.sh                      # Linux/Mac setup script
├── README.md                     # Full documentation
├── API_DOCUMENTATION.md          # API reference
└── QUICKSTART.md                 # This file!
```

---

## 🚀 Getting Started (5 Minutes)

### Option 1: Automatic Setup (Windows)

```powershell
cd C:\Users\susha\OneDrive\Desktop\disaster-management
setup.bat
```

The script will:
1. Create Python virtual environment
2. Install all dependencies
3. Initialize the database
4. Create sample admin user
5. Start the development server

Then visit: **http://localhost:5000**

### Option 2: Automatic Setup (Linux/Mac)

```bash
cd ~/disaster-management
chmod +x setup.sh
./setup.sh
```

### Option 3: Manual Setup

```powershell
# Navigate to project
cd C:\Users\susha\OneDrive\Desktop\disaster-management

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# OR source venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create database directory
mkdir database

# Run the app
python backend/app.py
```

**Server starts on:** `http://localhost:5000`

---

## 📧 Test Credentials

After setup, the following admin user is created:

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@disaster.com` | `admin123` |

Create additional test users via the **Sign Up** form in the UI.

---

## 🎯 Quick Test Workflow

### 1. Login as Admin
```
Email: admin@disaster.com
Password: admin123
```
- View dashboard statistics
- Manage disasters and resources
- Assign volunteers to tasks
- Send alerts

### 2. Create Citizen Account
- Go to **Sign Up** → select **Citizen**
- Submit a disaster report
- Track its status
- Receive alerts

### 3. Create Volunteer Account
- Go to **Sign Up** → select **Volunteer**
- Login and view your dashboard
- Check assigned tasks
- Update task progress

---

## 🔌 API Endpoints (Examples)

### Public Endpoints (No Auth Required)
```
GET  /api/public/disasters           # Active disasters
GET  /api/public/alerts               # Broadcast alerts
GET  /api/public/resources            # Available resources
GET  /api/public/statistics           # System stats
```

### Auth Endpoints
```
POST /api/auth/signup                # Register user
POST /api/auth/login                 # Login
POST /api/auth/logout                # Logout
GET  /api/auth/me                    # Current user
```

### Citizen Endpoints
```
GET  /api/citizen/dashboard          # Dashboard
GET  /api/citizen/reports            # My reports
POST /api/citizen/reports            # Submit report
GET  /api/citizen/alerts             # My alerts
```

### Volunteer Endpoints
```
GET  /api/volunteer/dashboard        # Task dashboard
GET  /api/volunteer/tasks            # My tasks
PATCH /api/volunteer/tasks/<id>      # Update task
POST /api/volunteer/tasks/<id>/start # Start task
```

### Admin Endpoints
```
GET  /api/admin/dashboard            # Admin stats
GET  /api/admin/reports              # All reports
POST /api/admin/reports/<id>/assign  # Assign volunteer
GET  /api/admin/resources            # Resource list
POST /api/admin/resources            # Create resource
GET  /api/admin/alerts               # Alerts list
POST /api/admin/alerts               # Send alert
```

---

## 📱 Frontend Features

### Home Page
- System overview with statistics
- View active disasters
- View recent alerts
- Quick access buttons

### User Authentication
- Sign Up with role selection
- Login with email/password
- Role-based navigation

### Citizen Dashboard
- Submit disaster reports
- View own reports
- Track status
- Receive alerts

### Admin Dashboard
- System statistics
- Manage all reports
- Assign volunteers
- Manage resources
- Send alerts

### Volunteer Dashboard
- View assigned tasks
- Update task status
- Track progress

---

## 🛠️ Environment Configuration

Edit `.env` file to customize:

```env
FLASK_APP=backend/app.py
FLASK_ENV=development              # Change to 'production' for deployment
SECRET_KEY=your-secret-key-here   # Change this in production!
DATABASE_URL=sqlite:///database/disaster.db
DEBUG=True                         # Set to False in production
```

---

## 🚢 Production Deployment

### Using Gunicorn (Recommended)

```powershell
# Install production server
pip install gunicorn

# Run with Gunicorn
python -m gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 wsgi:app
```

### Using Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_ENV=production
EXPOSE 5000
CMD ["python", "-m", "gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:5000", "wsgi:app"]
```

Build and run:
```bash
docker build -t disaster-management .
docker run -p 5000:5000 disaster-management
```

---

## 📚 Database Models

### User
```python
- id, name, email, password_hash, phone, location
- role: admin / volunteer / citizen
- is_active, timestamps
```

### DisasterReport
```python
- id, title, description, location, lat/lng
- severity: low / medium / high / critical
- status: pending / acknowledged / in_progress / resolved
- reporter_id, image_url
```

### VolunteerTask
```python
- id, volunteer_id, report_id, description
- status: assigned / in_progress / completed / failed
- timestamps
```

### Resource
```python
- id, name, type (medical/food/shelter/etc.)
- quantity, unit, location, availability
```

### Alert
```python
- id, title, message, level (info/warning/critical)
- report_id, is_broadcast, created_at
```

---

## 🐛 Troubleshooting

### Port 5000 Already in Use
```powershell
# Use different port
python backend/app.py --port 8000
```

### Database File Not Found
```powershell
mkdir database
# Then restart the app
```

### Module Not Found Errors
```powershell
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Flask App Import Errors
```powershell
# Check Python path
python -c "import sys; print(sys.path)"

# Verify app imports
python -c "from backend.app import app; print('✅ OK')"
```

---

## 📖 Documentation Files

- **README.md** - Complete project documentation
- **API_DOCUMENTATION.md** - Detailed API reference
- **QUICKSTART.md** - This file!

---

## 🎨 Key Features Implemented

✅ **Multi-Role System**
- Admin: Full system control
- Volunteer: Task management
- Citizen: Disaster reporting

✅ **Real-Time Features**
- Socket.IO support (ready for real-time updates)
- Broadcast alerts
- Live notifications

✅ **Data Management**
- Comprehensive disaster tracking
- Resource inventory
- Volunteer assignment
- Task status tracking

✅ **Security**
- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control
- CSRF protection ready

✅ **Responsive Design**
- Mobile-friendly UI
- Modern card-based layout
- Dark/Light mode ready
- Accessible forms

---

## 🚀 Next Steps

1. **Customize** - Modify models, add fields as needed
2. **Deploy** - Push to Heroku, AWS, DigitalOcean, etc.
3. **Integrate** - Connect to SMS/Email services
4. **Enhance** - Add real-time map updates, notifications
5. **Test** - Run comprehensive API tests

---

## 📞 Support

For issues or questions:
1. Check README.md for detailed docs
2. Review API_DOCUMENTATION.md for endpoints
3. Check error logs in console
4. Verify .env configuration

---

## 📄 License

MIT License - Free to use, modify, and deploy

---

**Built with ❤️ for disaster management and emergency response**

Happy coding! 🎉
