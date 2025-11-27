"""
Public API routes - for public access and real-time data
"""
from flask import Blueprint, request, jsonify
from models import DisasterReport, Alert, Resource, ReportStatus

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/public/disasters', methods=['GET'])
def get_active_disasters():
    """Get active/ongoing disaster reports (public)"""
    disasters = DisasterReport.query.filter(
        DisasterReport.status.in_([ReportStatus.PENDING, ReportStatus.IN_PROGRESS])
    ).order_by(DisasterReport.created_at.desc()).all()
    
    return {
        'disasters': [d.to_dict() for d in disasters],
        'total': len(disasters)
    }, 200


@api_bp.route('/public/alerts', methods=['GET'])
def get_public_alerts():
    """Get public broadcast alerts"""
    limit = request.args.get('limit', 20, type=int)
    alerts = Alert.query.filter_by(is_broadcast=True).order_by(
        Alert.created_at.desc()
    ).limit(limit).all()
    
    return {
        'alerts': [a.to_dict() for a in alerts],
        'total': len(alerts)
    }, 200


@api_bp.route('/public/resources', methods=['GET'])
def get_available_resources():
    """Get available resources (public)"""
    resource_type = request.args.get('type')
    
    query = Resource.query.filter_by(availability='available')
    
    if resource_type:
        query = query.filter_by(resource_type=resource_type)
    
    resources = query.all()
    
    return {
        'resources': [r.to_dict() for r in resources],
        'total': len(resources)
    }, 200


@api_bp.route('/public/statistics', methods=['GET'])
def get_statistics():
    """Get public statistics"""
    total_reports = DisasterReport.query.count()
    active_reports = DisasterReport.query.filter(
        DisasterReport.status.in_([ReportStatus.PENDING, ReportStatus.IN_PROGRESS])
    ).count()
    resolved_reports = DisasterReport.query.filter_by(status=ReportStatus.RESOLVED).count()
    total_resources = Resource.query.count()
    available_resources = Resource.query.filter_by(availability='available').count()
    
    return {
        'disaster_stats': {
            'total_reports': total_reports,
            'active_reports': active_reports,
            'resolved_reports': resolved_reports
        },
        'resource_stats': {
            'total': total_resources,
            'available': available_resources
        }
    }, 200
