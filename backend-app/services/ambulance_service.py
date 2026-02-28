from models.ambulance import Ambulance

def assign_ambulance(db, hospital_id: int):

    ambulance = db.query(Ambulance).filter(
        Ambulance.hospital_id == hospital_id,
        Ambulance.available == True
    ).first()

    if not ambulance:
        return None

    ambulance.available = False
    db.commit()

    return ambulance