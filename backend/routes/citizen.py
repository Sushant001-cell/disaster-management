"""
Citizen routes - submit reports, track status, receive alerts
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, DisasterReport, Alert, UserRole, ReportStatus, DisasterSeverity

citizen_bp = Blueprint('citizen', __name__, url_prefix='/api/citizen')


@citizen_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Citizen dashboard - their reports and active disasters"""
    my_reports = DisasterReport.query.filter_by(reporter_id=current_user.id).all()
    active_reports = DisasterReport.query.filter(
        DisasterReport.status.in_([ReportStatus.PENDING, ReportStatus.IN_PROGRESS])
    ).limit(10).all()
    recent_alerts = Alert.query.order_by(Alert.created_at.desc()).limit(5).all()
    
    return {
        'my_reports': [r.to_dict() for r in my_reports],
        'active_disasters': [r.to_dict() for r in active_reports],
        'recent_alerts': [a.to_dict() for a in recent_alerts]
    }, 200


@citizen_bp.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    """Get citizen's reports or submit new report"""
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        paginated = DisasterReport.query.filter_by(
            reporter_id=current_user.id
        ).order_by(DisasterReport.created_at.desc()).paginate(page=page, per_page=per_page)
        
        return {
            'reports': [r.to_dict() for r in paginated.items],
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': page
        }, 200
    
    else:  # POST - Submit new report
        data = request.get_json()
        
        required_fields = ['title', 'description', 'location']
        if not data or not all(field in data for field in required_fields):
            return {'error': 'Missing required fields'}, 400
        
        report = DisasterReport(
            title=data['title'],
            description=data['description'],
            location=data['location'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            severity=DisasterSeverity[data.get('severity', 'MEDIUM').upper()],
            reporter_id=current_user.id,
            image_url=data.get('image_url')
        )
        
        db.session.add(report)
        db.session.commit()
        
        return {
            'message': 'Report submitted successfully',
            'report': report.to_dict()
        }, 201


@citizen_bp.route('/reports/<int:report_id>', methods=['GET', 'PATCH'])
@login_required
def manage_report(report_id):
    """Get or update citizen's own report"""
    report = DisasterReport.query.get_or_404(report_id)
    
    # Check if citizen owns this report
    if report.reporter_id != current_user.id:
        return {'error': 'Unauthorized'}, 403
    
    if request.method == 'GET':
        return report.to_dict(include_tasks=True), 200
    
    else:  # PATCH
        data = request.get_json()
        
        if 'title' in data:
            report.title = data['title']
        if 'description' in data:
            report.description = data['description']
        if 'severity' in data:
            report.severity = DisasterSeverity[data['severity'].upper()]
        
        db.session.commit()
        return report.to_dict(), 200


@citizen_bp.route('/reports/<int:report_id>/status', methods=['GET'])
@login_required
def report_status(report_id):
    """Track status of report"""
    report = DisasterReport.query.get_or_404(report_id)
    
    if report.reporter_id != current_user.id:
        return {'error': 'Unauthorized'}, 403
    
    return {
        'report_id': report.id,
        'status': report.status.value,
        'title': report.title,
        'assigned_volunteers': len(report.volunteer_tasks),
        'last_update': report.updated_at.isoformat()
    }, 200


@citizen_bp.route('/alerts', methods=['GET'])
@login_required
def get_alerts():
    """Get alerts for citizen"""
    recent_alerts = Alert.query.filter(
        Alert.is_broadcast == True
    ).order_by(Alert.created_at.desc()).limit(20).all()
    
    return {
        'alerts': [a.to_dict() for a in recent_alerts],
        'total': len(recent_alerts)
    }, 200
