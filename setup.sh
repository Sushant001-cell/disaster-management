#!/bin/bash
# Quick setup and run script for Disaster Management System

echo "🚀 Disaster Management System Setup"
echo "===================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

echo "✅ Python 3 found"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate venv
echo "🔌 Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "🗄️ Initializing database..."
python3 << EOF
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

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Starting development server..."
echo "📍 Open http://localhost:5000 in your browser"
echo ""

python3 backend/app.py
