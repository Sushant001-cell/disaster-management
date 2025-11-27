"""
Volunteer routes - view tasks, update status
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from models import db, User, UserRole, VolunteerTask, TaskStatus

volunteer_bp = Blueprint('volunteer', __name__, url_prefix='/api/volunteer')


def volunteer_required(f):
    """Decorator to require volunteer role"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != UserRole.VOLUNTEER:
            return {'error': 'Volunteer access required'}, 403
        return f(*args, **kwargs)
    return decorated_function


@volunteer_bp.route('/dashboard', methods=['GET'])
@login_required
@volunteer_required
def dashboard():
    """Volunteer dashboard - assigned tasks"""
    tasks = VolunteerTask.query.filter_by(volunteer_id=current_user.id).all()
    
    assigned = len([t for t in tasks if t.status == TaskStatus.ASSIGNED])
    in_progress = len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS])
    completed = len([t for t in tasks if t.status == TaskStatus.COMPLETED])
    
    return {
        'total_tasks': len(tasks),
        'assigned': assigned,
        'in_progress': in_progress,
        'completed': completed,
        'recent_tasks': [t.to_dict() for t in tasks[-5:]]
    }, 200


@volunteer_bp.route('/tasks', methods=['GET'])
@login_required
@volunteer_required
def get_tasks():
    """Get all assigned tasks"""
    status = request.args.get('status')
    
    query = VolunteerTask.query.filter_by(volunteer_id=current_user.id)
    
    if status:
        query = query.filter_by(status=TaskStatus[status.upper()])
    
    tasks = query.order_by(VolunteerTask.assigned_at.desc()).all()
    
    return {
        'tasks': [t.to_dict() for t in tasks],
        'total': len(tasks)
    }, 200


@volunteer_bp.route('/tasks/<int:task_id>', methods=['GET', 'PATCH'])
@login_required
@volunteer_required
def manage_task(task_id):
    """Get or update specific task"""
    task = VolunteerTask.query.get_or_404(task_id)
    
    # Check if task belongs to current volunteer
    if task.volunteer_id != current_user.id:
        return {'error': 'Unauthorized'}, 403
    
    if request.method == 'GET':
        return task.to_dict(), 200
    
    else:  # PATCH
        data = request.get_json()
        
        if 'status' in data:
            new_status = TaskStatus[data['status'].upper()]
            task.status = new_status
            
            if new_status == TaskStatus.IN_PROGRESS and not task.started_at:
                task.started_at = datetime.utcnow()
            elif new_status == TaskStatus.COMPLETED:
                task.completed_at = datetime.utcnow()
        
        if 'notes' in data:
            task.notes = data['notes']
        
        db.session.commit()
        
        return {
            'message': 'Task updated successfully',
            'task': task.to_dict()
        }, 200


@volunteer_bp.route('/tasks/<int:task_id>/start', methods=['POST'])
@login_required
@volunteer_required
def start_task(task_id):
    """Start a task (mark as in_progress)"""
    task = VolunteerTask.query.get_or_404(task_id)
    
    if task.volunteer_id != current_user.id:
        return {'error': 'Unauthorized'}, 403
    
    if task.status != TaskStatus.ASSIGNED:
        return {'error': 'Task must be in ASSIGNED status'}, 400
    
    task.status = TaskStatus.IN_PROGRESS
    task.started_at = datetime.utcnow()
    db.session.commit()
    
    return {
        'message': 'Task started',
        'task': task.to_dict()
    }, 200


@volunteer_bp.route('/tasks/<int:task_id>/complete', methods=['POST'])
@login_required
@volunteer_required
def complete_task(task_id):
    """Mark task as completed"""
    task = VolunteerTask.query.get_or_404(task_id)
    
    if task.volunteer_id != current_user.id:
        return {'error': 'Unauthorized'}, 403
    
    if task.status == TaskStatus.COMPLETED:
        return {'error': 'Task already completed'}, 400
    
    task.status = TaskStatus.COMPLETED
    task.completed_at = datetime.utcnow()
    db.session.commit()
    
    return {
        'message': 'Task marked as completed',
        'task': task.to_dict()
    }, 200
