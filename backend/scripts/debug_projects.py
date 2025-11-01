import sys
import os
from datetime import datetime, timezone
from typing import List

# Ensure parent directory (backend) is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal
from app.models.project import Project, ProjectStatus


def scan_projects() -> List[Project]:
    db = SessionLocal()
    try:
        return db.query(Project).order_by(Project.id.asc()).all()
    finally:
        db.close()


def main():
    projects = scan_projects()
    print(f"Total projects: {len(projects)}")

    anomalies = []
    for p in projects:
        status_val = p.status
        created_ok = isinstance(p.created_at, datetime)
        updated_ok = (p.updated_at is None) or isinstance(p.updated_at, datetime)
        status_ok = isinstance(status_val, ProjectStatus)
        leader_ok = isinstance(p.leader_id, int) or p.leader_id is None
        tags_ok = (p.tags is None) or isinstance(p.tags, str)

        row_info = {
            "id": p.id,
            "name": p.name,
            "leader_id": p.leader_id,
            "status": str(status_val) if status_val is not None else None,
            "created_at": p.created_at,
            "updated_at": p.updated_at,
            "tags_type": type(p.tags).__name__ if p.tags is not None else None,
        }

        issues = []
        if not created_ok or p.created_at is None:
            issues.append("created_at_missing_or_invalid")
        if not updated_ok:
            issues.append("updated_at_invalid")
        if not status_ok or status_val is None:
            issues.append("status_invalid_or_null")
        if not leader_ok:
            issues.append("leader_id_invalid_type")
        if not tags_ok:
            issues.append("tags_invalid_type")

        if issues:
            anomalies.append({"row": row_info, "issues": issues})

    if not anomalies:
        print("No anomalies detected.")
    else:
        print(f"Anomalies detected: {len(anomalies)}")
        for a in anomalies:
            print(a)

    # Exit code reflects whether anomalies exist
    sys.exit(1 if anomalies else 0)


if __name__ == "__main__":
    main()