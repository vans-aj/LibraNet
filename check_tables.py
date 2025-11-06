from app import create_app, db
from sqlalchemy import inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print("Tables in database:")
    for table in sorted(tables):
        print(f"  - {table}")
    
    if 'user' in tables:
        print("\n✓ 'user' table exists!")
    if 'student' in tables:
        print("\n✗ 'student' table still exists!")
