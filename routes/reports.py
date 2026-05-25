from flask import Blueprint, jsonify, request
from models import db, Report, ReportStatus, Status, Priority
from schemas import serialize_report

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/api/reports', methods=['GET'])
def get_reports():
    status_filter = request.args.get('status')
    if status_filter:
        try:
            status_enum = Status[status_filter.upper()]
            reports = Report.query.filter_by(status=status_enum).all()
        except KeyError:
            return jsonify({"error": "Estado inválido. Use OPEN, IN_PROGRESS o CLOSED"}), 400
    else:
        reports = Report.query.all()

    return jsonify({
        "reports": [serialize_report(r) for r in reports],
        "total": len(reports)
    }), 200

@reports_bp.route('/api/reports/<int:id>', methods=['GET'])
def get_report(id):
    report = Report.query.get(id)
    if not report:
        return jsonify({"error": f"Reporte con id {id} no encontrado"}), 404
    return jsonify(serialize_report(report)), 200

@reports_bp.route('/api/reports', methods=['POST'])
def create_report():
    data = request.get_json()

    required_fields = ['title', 'description', 'category_id', 'user_id']
    for field in required_fields:
        if not data or not data.get(field):
            return jsonify({"error": f"El campo '{field}' es obligatorio"}), 400

    try:
        priority = Priority[data.get('priority', 'MEDIUM').upper()]
    except KeyError:
        return jsonify({"error": "Prioridad inválida. Use LOW, MEDIUM o HIGH"}), 400

    new_report = Report(
        title=data['title'],
        description=data['description'],
        category_id=data['category_id'],
        user_id=data['user_id'],
        priority=priority,
        status=Status.OPEN,
        location=data.get('location'),
        is_synced=True
    )

    db.session.add(new_report)
    db.session.commit()

    return jsonify(serialize_report(new_report)), 201

@reports_bp.route('/api/reports/<int:id>', methods=['PUT'])
def update_report(id):
    report = Report.query.get(id)
    if not report:
        return jsonify({"error": f"Reporte con id {id} no encontrado"}), 404

    data = request.get_json()

    if 'title' in data:
        report.title = data['title']
    if 'description' in data:
        report.description = data['description']
    if 'location' in data:
        report.location = data['location']
    if 'priority' in data:
        try:
            report.priority = Priority[data['priority'].upper()]
        except KeyError:
            return jsonify({"error": "Prioridad inválida. Use LOW, MEDIUM o HIGH"}), 400
    if 'status' in data:
        try:
            new_status = Status[data['status'].upper()]
            report.status = new_status
            status_log = ReportStatus(
                report_id=report.id,
                status=new_status,
                note=data.get('note')
            )
            db.session.add(status_log)
        except KeyError:
            return jsonify({"error": "Estado inválido. Use OPEN, IN_PROGRESS o CLOSED"}), 400

    db.session.commit()

    return jsonify(serialize_report(report)), 200