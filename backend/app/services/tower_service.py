from app.models import Tower
from app.extensions.db import db
def create_tower(data):

    name = data.get("name")
    code = data.get("code")
    locality=data.get("locality")

    if not name or not code:
        raise ValueError("Tower name and code are required")
    
    existing = Tower.query.filter_by(code=code).first()
    if existing:        
        raise ValueError("Tower with this code already exists")
    
    tower = Tower(name=name,code=code.upper(), locality=locality)
    db.session.add(tower)
    db.session.commit()

    return tower



def get_all_towers():
    return Tower.query.all()


def get_tower_by_code_service(code):
    return Tower.query.filter_by(code=code.upper()).first()



# def get_tower_by_code(code):
#     tower = Tower.query.filter_by(code=code.upper()).first()
#     return tower

def update_tower(code,data):
    tower=Tower.query.filter_by(code=code.upper()).first()

    if not tower:
        raise ValueError("Tower not found")
    
    if data.get("name"):
        tower.name=data["name"]

    if data.get("locality"):
        tower.locality=data["locality"]

    if data.get("code"):
        existing = Tower.query.filter_by(code=data["code"]).first()
        if existing and existing.id != tower.id:
            raise ValueError("Another tower with this code already exists")
        tower.code=data["code"].upper()
    

    db.session.commit()
    return tower


def delete_tower(code):
    tower = Tower.query.filter_by(code=code.upper()).first()

    if not tower:
        raise ValueError("Tower not found")
    
    db.session.delete(tower)
    db.session.commit()