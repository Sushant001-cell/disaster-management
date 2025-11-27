@echo off
REM Quick setup and run script for Windows

echo 🚀 Disaster Management System Setup
echo ====================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.9+
    exit /b 1
)

echo ✅ Python found
echo.

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate venv
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Initialize database
echo 🗄️ Initializing database...
python << EOF
from backend.app import app, db
from backend.models import init_db, User, UserRole

init_db(app)

# Create sample admin user
admin = User(
    name='Admin User',
    email='admin@disaster.com',
    phone='9999999999',
    role=UserRole.ADMIN
)
admin.set_password('admin123')

db.session.add(admin)
db.session.commit()

print("✅ Database initialized!")
print("✅ Sample admin user created!")
print("   Email: admin@disaster.com")
print("   Password: admin123")
EOF

echo.
echo ✅ Setup complete!
echo.
echo 🌐 Starting development server...
echo 📍 Open http://localhost:5000 in your browser
echo.

python backend/app.py
