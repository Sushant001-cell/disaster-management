"""
Database models for Disaster Management System
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
import enum

db = SQLAlchemy()


class UserRole(enum.Enum):
    """User roles in the system"""
    ADMIN = "admin"
    VOLUNTEER = "volunteer"
    CITIZEN = "citizen"


class DisasterSeverity(enum.Enum):
    """Disaster severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ReportStatus(enum.Enum):
    """Disaster report status"""
    PENDING = "pending"
    ACKNOWLEDGED = "acknowledged"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CANCELLED = "cancelled"


class TaskStatus(enum.Enum):
    """Volunteer task status"""
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class User(UserMixin, db.Model):
    """User model for all roles"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    location = db.Column(db.String(255))
    role = db.Column(db.Enum(UserRole), default=UserRole.CITIZEN, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    reports = db.relationship('DisasterReport', backref='reporter', lazy=True, foreign_keys='DisasterReport.reporter_id')
    volunteer_tasks = db.relationship('VolunteerTask', backref='volunteer', lazy=True, foreign_keys='VolunteerTask.volunteer_id')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'role': self.role.value,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }


class DisasterReport(db.Model):
    """Disaster report model"""
    __tablename__ = 'disaster_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    severity = db.Column(db.Enum(DisasterSeverity), default=DisasterSeverity.MEDIUM)
    status = db.Column(db.Enum(ReportStatus), default=ReportStatus.PENDING)
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    resolved_at = db.Column(db.DateTime)
    
    # Relationships
    volunteer_tasks = db.relationship('VolunteerTask', backref='report', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('Alert', backref='report', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_tasks=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'severity': self.severity.value,
            'status': self.status.value,
            'reporter': self.reporter.to_dict() if self.reporter else None,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }
        if include_tasks:
            data['volunteer_tasks'] = [t.to_dict() for t in self.volunteer_tasks]
        return data


class VolunteerTask(db.Model):
    """Volunteer task assignment model"""
    __tablename__ = 'volunteer_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('disaster_reports.id'), nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.ASSIGNED)
    assigned_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'volunteer': self.volunteer.to_dict() if self.volunteer else None,
            'report_id': self.report_id,
            'task_description': self.task_description,
            'status': self.status.value,
            'assigned_at': self.assigned_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'notes': self.notes
        }


class Resource(db.Model):
    """Emergency resources model"""
    __tablename__ = 'resources'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    resource_type = db.Column(db.String(100), nullable=False)  # medical, food, shelter, transport, etc.
    quantity = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(50))  # units, liters, kg, beds, etc.
    location = db.Column(db.String(255))
    availability = db.Column(db.String(50), default='available')  # available, in_use, exhausted
    contact_person = db.Column(db.String(255))
    contact_phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'resource_type': self.resource_type,
            'quantity': self.quantity,
            'unit': self.unit,
            'location': self.location,
            'availability': self.availability,
            'contact_person': self.contact_person,
            'contact_phone': self.contact_phone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Alert(db.Model):
    """Alert/notification model"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    alert_level = db.Column(db.String(50), default='info')  # info, warning, critical
    report_id = db.Column(db.Integer, db.ForeignKey('disaster_reports.id'))
    target_role = db.Column(db.Enum(UserRole), default=UserRole.CITIZEN)  # who to notify
    is_broadcast = db.Column(db.Boolean, default=False)  # broadcast to all users
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'alert_level': self.alert_level,
            'report_id': self.report_id,
            'target_role': self.target_role.value,
            'is_broadcast': self.is_broadcast,
            'created_at': self.created_at.isoformat()
        }


def init_db(app):
    """Initialize database with app context"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
