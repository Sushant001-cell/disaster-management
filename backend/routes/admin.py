"""
Admin routes - manage reports, volunteers, resources, and alerts
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from functools import wraps
from models import (
    db, User, UserRole, DisasterReport, VolunteerTask, Resource, Alert,
    TaskStatus, ReportStatus, DisasterSeverity
)

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != UserRole.ADMIN:
            return {'error': 'Admin access required'}, 403
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard', methods=['GET'])
@login_required
@admin_required
def dashboard():
    """Admin dashboard statistics"""
    total_reports = DisasterReport.query.count()
    pending_reports = DisasterReport.query.filter_by(status=ReportStatus.PENDING).count()
    active_volunteers = User.query.filter_by(role=UserRole.VOLUNTEER).count()
    total_resources = Resource.query.count()
    
    return {
        'total_reports': total_reports,
        'pending_reports': pending_reports,
        'active_volunteers': active_volunteers,
        'total_resources': total_resources
    }, 200


@admin_bp.route('/reports', methods=['GET'])
@login_required
@admin_required
def get_all_reports():
    """Get all disaster reports"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    
    query = DisasterReport.query.order_by(DisasterReport.created_at.desc())
    
    if status:
        query = query.filter_by(status=ReportStatus[status.upper()])
    
    paginated = query.paginate(page=page, per_page=per_page)
    
    return {
        'reports': [r.to_dict(include_tasks=True) for r in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': page
    }, 200


@admin_bp.route('/reports/<int:report_id>', methods=['GET'])
@login_required
@admin_required
def get_report(report_id):
    """Get specific report details"""
    report = DisasterReport.query.get_or_404(report_id)
    return report.to_dict(include_tasks=True), 200


@admin_bp.route('/reports/<int:report_id>/status', methods=['PATCH'])
@login_required
@admin_required
def update_report_status(report_id):
    """Update report status"""
    report = DisasterReport.query.get_or_404(report_id)
    data = request.get_json()
    
    if 'status' not in data:
        return {'error': 'Status field required'}, 400
    
    try:
        new_status = ReportStatus[data['status'].upper()]
        report.status = new_status
        db.session.commit()
        return report.to_dict(), 200
    except KeyError:
        return {'error': 'Invalid status'}, 400


@admin_bp.route('/reports/<int:report_id>/assign', methods=['POST'])
@login_required
@admin_required
def assign_volunteer(report_id):
    """Assign volunteer to disaster report"""
    report = DisasterReport.query.get_or_404(report_id)
    data = request.get_json()
    
    if not data or 'volunteer_id' not in data or 'task_description' not in data:
        return {'error': 'Missing volunteer_id or task_description'}, 400
    
    volunteer = User.query.get_or_404(data['volunteer_id'])
    
    if volunteer.role != UserRole.VOLUNTEER:
        return {'error': 'Selected user is not a volunteer'}, 400
    
    task = VolunteerTask(
        volunteer_id=volunteer.id,
        report_id=report.id,
        task_description=data['task_description']
    )
    
    db.session.add(task)
    db.session.commit()
    
    return {
        'message': 'Volunteer assigned successfully',
        'task': task.to_dict()
    }, 201


@admin_bp.route('/volunteers', methods=['GET'])
@login_required
@admin_required
def get_volunteers():
    """Get all volunteers"""
    volunteers = User.query.filter_by(role=UserRole.VOLUNTEER).all()
    return {
        'volunteers': [v.to_dict() for v in volunteers],
        'total': len(volunteers)
    }, 200


@admin_bp.route('/resources', methods=['GET', 'POST'])
@login_required
@admin_required
def resources():
    """Get all resources or create new resource"""
    if request.method == 'GET':
        resources = Resource.query.all()
        return {
            'resources': [r.to_dict() for r in resources],
            'total': len(resources)
        }, 200
    
    else:  # POST
        data = request.get_json()
        
        if not data or not data.get('name') or not data.get('resource_type'):
            return {'error': 'Missing required fields'}, 400
        
        resource = Resource(
            name=data['name'],
            resource_type=data['resource_type'],
            quantity=data.get('quantity', 0),
            unit=data.get('unit'),
            location=data.get('location'),
            contact_person=data.get('contact_person'),
            contact_phone=data.get('contact_phone')
        )
        
        db.session.add(resource)
        db.session.commit()
        
        return {
            'message': 'Resource created successfully',
            'resource': resource.to_dict()
        }, 201


@admin_bp.route('/resources/<int:resource_id>', methods=['GET', 'PATCH', 'DELETE'])
@login_required
@admin_required
def manage_resource(resource_id):
    """Get, update, or delete resource"""
    resource = Resource.query.get_or_404(resource_id)
    
    if request.method == 'GET':
        return resource.to_dict(), 200
    
    elif request.method == 'PATCH':
        data = request.get_json()
        
        if 'name' in data:
            resource.name = data['name']
        if 'quantity' in data:
            resource.quantity = data['quantity']
        if 'availability' in data:
            resource.availability = data['availability']
        if 'location' in data:
            resource.location = data['location']
        
        db.session.commit()
        return resource.to_dict(), 200
    
    else:  # DELETE
        db.session.delete(resource)
        db.session.commit()
        return {'message': 'Resource deleted'}, 200


@admin_bp.route('/alerts', methods=['GET', 'POST'])
@login_required
@admin_required
def alerts():
    """Get alerts or create new alert"""
    if request.method == 'GET':
        alerts = Alert.query.order_by(Alert.created_at.desc()).limit(50).all()
        return {
            'alerts': [a.to_dict() for a in alerts],
            'total': len(alerts)
        }, 200
    
    else:  # POST - Create new alert
        data = request.get_json()
        
        if not data or not data.get('title') or not data.get('message'):
            return {'error': 'Missing title or message'}, 400
        
        alert = Alert(
            title=data['title'],
            message=data['message'],
            alert_level=data.get('alert_level', 'info'),
            report_id=data.get('report_id'),
            is_broadcast=data.get('is_broadcast', True)
        )
        
        db.session.add(alert)
        db.session.commit()
        
        # TODO: Emit socket.io event to broadcast alert
        
        return {
            'message': 'Alert created successfully',
            'alert': alert.to_dict()
        }, 201
