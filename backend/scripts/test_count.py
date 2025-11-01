import os
import sys

# Ensure parent directory (backend) is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal
from app.models.project import Project
from sqlalchemy.exc import SQLAlchemyError


def main():
    sess = SessionLocal()
    try:
        q = sess.query(Project)
        try:
            print('count_no_order', q.count())
        except SQLAlchemyError as e:
            print('count_no_order_error', type(e).__name__, e)

        q2 = q.order_by(Project.created_at.desc())
        try:
            print('count_with_order', q2.count())
        except SQLAlchemyError as e:
            print('count_with_order_error', type(e).__name__, e)
    finally:
        sess.close()


if __name__ == '__main__':
    main()