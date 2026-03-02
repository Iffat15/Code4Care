from models.ambulance import Ambulance

# ---------------------------------------------------------
# Assign Ambulance to a Booking
# ---------------------------------------------------------
# Business Logic:
# 1. Find first available ambulance for the given hospital.
# 2. If none available → return None.
# 3. If available → mark ambulance as unavailable.
# 4. Commit change immediately to prevent double assignment.
#
# Used during:
# - Booking approval process
#
# Returns:
# - Ambulance object if successfully assigned
# - None if no ambulance available
def assign_ambulance(db, hospital_id: int):

    # Step 1: Find available ambulance in the same hospital
    ambulance = db.query(Ambulance).filter(
        Ambulance.hospital_id == hospital_id,
        Ambulance.available == True
    ).first()

    # Step 2: If no ambulance available, return None
    if not ambulance:
        return None

    # Step 3: Mark ambulance as unavailable (reserved)
    # This prevents multiple bookings from using same ambulance
    ambulance.available = False
    
    # Step 4: Save change immediately
    db.commit()

    return ambulance