# # from agents.triage_agent import run_triage
# # from services.hospital_service import find_available_bed
# # from models.booking import Booking

# # # ---------------------------------------------------------
# # # Process SOS Request
# # # ---------------------------------------------------------
# # # Business Flow:
# # # 1. Run AI triage on symptoms → determine severity level.
# # # 2. Find available bed based on severity.
# # # 3. If no beds available → return failure response.
# # # 4. Reduce available bed count (temporary reservation).
# # # 5. Create booking with status = "pending".
# # # 6. Return booking ID for admin approval workflow.
# # #
# # # NOTE:
# # # - Ambulance is NOT assigned here.
# # # - Ambulance assignment happens only after admin approval.
# # # - Bed is reduced immediately to prevent overbooking.
# # def process_sos(db, patient_name: str, symptoms: str, ambulance_requested: bool):
# #     #find hospital
    
# #     # Step 1: Determine severity using triage agent
# #     # Example output: {"severity": "high"} or {"severity": "medium"}
# #     triage_result = run_triage(symptoms)
# #     severity = triage_result["severity"]
    
# #     #find the available beds in hospital
# #     # Step 2: Find available bed based on severity
# #     # High severity → ICU
# #     # Medium/Low severity → General
# #     bed = find_available_bed(db, severity)

# #     # Step 3: If no bed available, stop process
# #     if not bed:
# #         return {"message": "No beds available"}

# #     # Step 4: Reserve bed immediately
# #     # This prevents race conditions where multiple users book same bed
# #     bed.available -= 1

# #     #book a bed in the hospital
# #     # Step 5: Create booking entry (awaiting admin approval)
# #     booking = Booking(
# #         patient_name=patient_name,
# #         hospital_id=bed.hospital_id,
# #         severity=severity,
# #         ambulance_requested=ambulance_requested,
# #         status="pending"
# #     )

# #     db.add(booking)
# #     db.commit()
# #     db.refresh(booking)

# #     # Step 6: Return confirmation response
# #     return {
# #         "message": "Booking created. Awaiting admin approval.",
# #         "booking_id": booking.id,
# #         "ambulance_requested": ambulance_requested
# #     }


# # services/sos_service.py

# from sqlalchemy.orm import Session
# from models.booking import Booking
# from models.bed import Bed
# from models.hospital import Hospital

# from agents.sos_agent import run_sos_agent
# from agents.triage_agent import run_triage
# from agents.orchestrator_agent import run_orchestration


# # ---------------------------------------------------------
# # Process SOS Request (Multi-Agent Orchestrated Flow)
# # ---------------------------------------------------------
# def process_sos(
#     db: Session,
#     patient_name: str,
#     symptoms: str,
#     ambulance_requested: bool,
#     patient_location_km: float  # distance simulation input
# ):
#     """
#     Multi-Agent SOS Processing Flow:

#     1. SOS Agent → Understand emergency intent
#     2. Triage Agent → Decide medical requirements
#     3. Orchestrator Agent → Select best hospital
#     4. Deterministic Layer → Reserve bed + create booking
#     """

#     # =====================================================
#     # STEP 1️⃣  SOS AGENT (Intent Understanding)
#     # =====================================================
#     sos_context = run_sos_agent(
#         symptoms=symptoms,
#         ambulance_requested=ambulance_requested
#     )

#     # =====================================================
#     # STEP 2️⃣  TRIAGE AGENT (Medical Reasoning)
#     # =====================================================
#     triage_decision = run_triage(
#         symptoms=symptoms,
#         context=sos_context
#     )

#     required_bed_type = triage_decision["required_bed_type"]

#     # =====================================================
#     # STEP 3️⃣  PREPARE HOSPITAL OPTIONS (Deterministic Fetch)
#     # =====================================================
#     # Fetch all hospitals with required bed type
#     beds = db.query(Bed).filter(
#         Bed.bed_type == required_bed_type,
#         Bed.available > 0
#     ).all()

#     hospital_options = []

#     for bed in beds:
#         hospital = db.query(Hospital).filter(
#             Hospital.id == bed.hospital_id
#         ).first()

#         # Simulated load factor (can later be computed properly)
#         load_factor = 1 - (bed.available / (bed.available + 5))

#         hospital_options.append({
#             "hospital_id": hospital.id,
#             "distance_km": patient_location_km + hospital.id,  # simple simulation
#             "available_beds": bed.available,
#             "bed_type": bed.bed_type,
#             "load_factor": load_factor
#         })

#     # =====================================================
#     # STEP 4️⃣  ORCHESTRATION AGENT (Hospital Decision)
#     # =====================================================
#     orchestration_result = run_orchestration(
#         triage_decision=triage_decision,
#         hospital_options=hospital_options
#     )

#     if not orchestration_result["hospital_id"]:
#         return {
#             "message": "No hospitals available for required bed type"
#         }

#     selected_hospital_id = orchestration_result["hospital_id"]

#     # =====================================================
#     # STEP 5️⃣  RESERVE BED (Deterministic Execution)
#     # =====================================================
#     selected_bed = db.query(Bed).filter(
#         Bed.hospital_id == selected_hospital_id,
#         Bed.bed_type == required_bed_type,
#         Bed.available > 0
#     ).first()

#     if not selected_bed:
#         return {
#             "message": "Selected hospital no longer has available beds"
#         }

#     # Reserve bed immediately
#     selected_bed.available -= 1

#     # =====================================================
#     # STEP 6️⃣  CREATE BOOKING (Audit-Ready)
#     # =====================================================
#     booking = Booking(
#         patient_name=patient_name,
#         hospital_id=selected_hospital_id,
#         severity=sos_context["urgency"],
#         ambulance_requested=sos_context["needs_ambulance"],
#         status="pending",
#         triage_level=required_bed_type,
#         confidence_score=triage_decision["confidence"],
#         ai_reasoning={
#             "sos_context": sos_context,
#             "triage_decision": triage_decision,
#             "orchestration_decision": orchestration_result
#         }
#     )

#     db.add(booking)
#     db.commit()
#     db.refresh(booking)

#     # =====================================================
#     # RESPONSE
#     # =====================================================
#     return {
#         "message": "Booking created. Awaiting admin approval.",
#         "booking_id": booking.id,
#         "selected_hospital": selected_hospital_id,
#         "bed_type": required_bed_type,
#         "ambulance_requested": sos_context["needs_ambulance"],
#         "confidence_score": triage_decision["confidence"]
#     }


# services/sos_service.py

from sqlalchemy.orm import Session
from models.booking import Booking
from models.bed import Bed
from models.hospital import Hospital
from models.ambulance import Ambulance

from services.orchestration_service import run_full_orchestration


# ==========================================================
# PROCESS SOS (CLEAN ARCHITECTURE VERSION)
# ==========================================================
def process_sos(
    db: Session,
    patient_name: str,
    symptoms: str,
    ambulance_requested: bool,
    patient_location_km: float
):
    """
    Clean SOS Flow:

    1️⃣ Fetch deterministic data (hospitals, beds, ambulances)
    2️⃣ Call orchestration layer
    3️⃣ Validate decisions
    4️⃣ Reserve bed
    5️⃣ Create booking with AI audit trail
    """

    # ======================================================
    # STEP 1️⃣ FETCH HOSPITAL OPTIONS (Deterministic)
    # ======================================================
    beds = db.query(Bed).filter(Bed.available > 0).all()

    hospital_options = []

    for bed in beds:
        hospital = db.query(Hospital).filter(
            Hospital.id == bed.hospital_id
        ).first()

        if not hospital:
            continue

        load_factor = 1 - (bed.available / (bed.available + 5))

        hospital_options.append({
            "hospital_id": hospital.id,
            "distance_km": patient_location_km + hospital.id,  # replace with real geo calc later
            "available_beds": bed.available,
            "bed_type": bed.bed_type,
            "load_factor": load_factor
        })

    # ======================================================
    # STEP 2️⃣ FETCH AMBULANCE OPTIONS
    # ======================================================
    ambulances = db.query(Ambulance).filter(
        Ambulance.available == True
    ).all()

    ambulance_options = []

    for amb in ambulances:
        ambulance_options.append({
            "ambulance_id": amb.id,
            "provider_type": amb.provider_type,  # "hospital" / "ngo"
            "support_type": amb.support_type,    # "ALS" / "BLS"
            "available": amb.available,
            "distance_km": patient_location_km + amb.id  # replace with geo later
        })

    # ======================================================
    # STEP 3️⃣ RUN FULL AI ORCHESTRATION
    # ======================================================
    decision_bundle = run_full_orchestration(
        symptoms=symptoms,
        ambulance_requested=ambulance_requested,
        hospital_options=hospital_options,
        ambulance_options=ambulance_options
    )

    hospital_decision = decision_bundle["hospital_decision"]
    ambulance_decision = decision_bundle["ambulance_decision"]
    triage_decision = decision_bundle["triage_decision"]
    sos_context = decision_bundle["sos_context"]

    # ======================================================
    # STEP 4️⃣ VALIDATE HOSPITAL DECISION
    # ======================================================
    if not hospital_decision or not hospital_decision.get("hospital_id"):
        return {
            "message": "No suitable hospital available",
            "ai_decision": decision_bundle
        }

    selected_hospital_id = hospital_decision["hospital_id"]
    required_bed_type = triage_decision["required_bed_type"]

    # ======================================================
    # STEP 5️⃣ RESERVE BED (ATOMIC DB ACTION)
    # ======================================================
    selected_bed = db.query(Bed).filter(
        Bed.hospital_id == selected_hospital_id,
        Bed.bed_type == required_bed_type,
        Bed.available > 0
    ).first()

    if not selected_bed:
        return {
            "message": "Selected hospital no longer has available beds",
            "ai_decision": decision_bundle
        }

    selected_bed.available -= 1

    # ======================================================
    # STEP 6️⃣ CREATE BOOKING
    # ======================================================
    booking = Booking(
        patient_name=patient_name,
        hospital_id=selected_hospital_id,
        severity=sos_context["urgency"],
        ambulance_requested=sos_context["needs_ambulance"],
        status="pending",
        triage_level=required_bed_type,
        confidence_score=decision_bundle["final_confidence"],
        ai_reasoning=decision_bundle  # full structured trace
    )

    db.add(booking)

    # ======================================================
    # STEP 7️⃣ OPTIONAL: PRE-RESERVE AMBULANCE (SOFT LOCK)
    # ======================================================
    if ambulance_decision and ambulance_decision.get("ambulance_id"):
        selected_ambulance = db.query(Ambulance).filter(
            Ambulance.id == ambulance_decision["ambulance_id"],
            Ambulance.available == True
        ).first()

        if selected_ambulance:
            selected_ambulance.available = False
            booking.ambulance_id = selected_ambulance.id

    db.commit()
    db.refresh(booking)

    # ======================================================
    # RESPONSE
    # ======================================================
    return {
        "message": "Booking created successfully",
        "booking_id": booking.id,
        "hospital_id": selected_hospital_id,
        "bed_type": required_bed_type,
        "ambulance_id": booking.ambulance_id,
        "confidence_score": decision_bundle["final_confidence"]
    }