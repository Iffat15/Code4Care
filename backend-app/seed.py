from database import SessionLocal, engine, Base
from models.hospital import Hospital
from models.bed import Bed
from models.ambulance import Ambulance

# 🔥 CREATE TABLES FIRST
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Create Hospital
hospital = Hospital(name="City Hospital", location="Pune")
db.add(hospital)
db.commit()
db.refresh(hospital)

# Create Beds
icu = Bed(hospital_id=hospital.id, bed_type="ICU", available=5)
general = Bed(hospital_id=hospital.id, bed_type="General", available=10)

db.add_all([icu, general])
db.commit()

# Create Ambulances
ambulance1 = Ambulance(
    hospital_id=hospital.id,
    driver_name="Ramesh",
    available=True
)

ambulance2 = Ambulance(
    hospital_id=hospital.id,
    driver_name="Suresh",
    available=True
)

db.add_all([ambulance1, ambulance2])
db.commit()

print("Seeded successfully with beds and ambulances 🚑")