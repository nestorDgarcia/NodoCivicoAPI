from models import db, User, Category, Report, ReportStatus, Reminder

def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "zone": user.zone,
        "email": user.email,
        "created_at": user.created_at.strftime("%Y-%m-%dT%H:%M:%S")
    }

def serialize_category(category):
    return {
        "id": category.id,
        "name": category.name,
        "icon": category.icon,
        "color_hex": category.color_hex
    }

def serialize_report(report):
    return {
        "id": report.id,
        "title": report.title,
        "description": report.description,
        "category_id": report.category_id,
        "category": report.category.name if report.category else None,
        "user_id": report.user_id,
        "priority": report.priority.value,
        "status": report.status.value,
        "location": report.location,
        "is_synced": report.is_synced,
        "created_at": report.created_at.strftime("%Y-%m-%dT%H:%M:%S")
    }

def serialize_report_status(rs):
    return {
        "id": rs.id,
        "report_id": rs.report_id,
        "status": rs.status.value,
        "note": rs.note,
        "changed_at": rs.changed_at.strftime("%Y-%m-%dT%H:%M:%S")
    }