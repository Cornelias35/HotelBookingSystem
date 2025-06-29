from sqlalchemy.orm import Session
from app.models.data_models import AdminDB, AdminDTO

def add_admin(db: Session, admin : AdminDTO):
    new_admin = AdminDB(
        username=admin.username,
        password=admin.password
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin