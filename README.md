## 📊 Database Structure Overview

The application uses a relational database designed to manage emergency medical requests, hospital availability, and ambulance dispatch efficiently.

---
Below is the Entity-Relationship (ER) diagram representing the database structure:

![Database ER Diagram](/backend-app/assets/database_diagram_er.png)
### 🧩 Core Entities

#### 1️⃣ Users
Stores verified users identified by their phone number.

- `id` (Primary Key)
- `phone_number` (Unique)
- `is_verified`
- `created_at`

A user can create multiple emergency requests and manage multiple patient profiles.

---

#### 2️⃣ Patients
Represents individuals for whom emergency care may be requested.  
A patient can either be the user themselves or someone else.

- `id` (Primary Key)
- `user_id` (Foreign Key → Users)
- `full_name`
- `age`
- `blood_group`
- `emergency_contact`
- `relation`
- `critical_information`
- `is_self`

Each patient belongs to exactly one user.

---

#### 3️⃣ Bookings (Emergency Requests)
Central transactional table representing an SOS request.

- `id` (Primary Key)
- `user_id` (Foreign Key → Users)
- `patient_id` (Foreign Key → Patients)
- `hospital_id` (Foreign Key → Hospitals)
- `ambulance_id` (Foreign Key → Ambulances, nullable)
- `severity`
- `ambulance_requested`
- `user_latitude`
- `user_longitude`
- `status`
- `created_at`
- `approved_at`
- `completed_at`

Each booking links:
- A user  
- A patient  
- A selected hospital  
- An optional ambulance  

---

#### 4️⃣ Hospitals
Stores hospital details and location data.

- `id` (Primary Key)
- `name`
- `latitude`
- `longitude`
- `rating`

A hospital can handle multiple emergency bookings.

---

#### 5️⃣ Bed Inventory
Maintains real-time bed availability for each hospital.

- `id` (Primary Key)
- `hospital_id` (Foreign Key → Hospitals)
- `bed_type` (ICU, Emergency, General)
- `total_beds`
- `available_beds`

Each hospital can have multiple bed inventory records (one per bed type).

---

#### 6️⃣ Ambulances
Stores ambulance and driver information.

- `id` (Primary Key)
- `hospital_id` (Foreign Key → Hospitals) or ngo_id
- `driver_name`
- `driver_phone`
- `latitude`
- `longitude`

Each ambulance belongs to one hospital and can serve multiple bookings over time.

---


### 🆕 NGO Ambulance Support

The system supports ambulances from both hospitals and partner NGOs.

- One **Hospital** → Many **Ambulances**
- One **NGO** → Many **Ambulances**
- One **Ambulance** → Many **Bookings** (historically)

An ambulance belongs to either:
- A hospital
- OR an NGO partner

During SOS dispatch:
1. The system searches for the nearest available hospital ambulance.
2. If none are available, it searches for the nearest available NGO ambulance.
3. The closest available ambulance is assigned to the booking.

---

## 🔗 Relationship Summary

- One **User** → Many **Patients**
- One **User** → Many **Bookings**
- One **Patient** → Many **Bookings**
- One **Hospital** → Many **Bookings**
- One **Hospital** → Many **Bed Inventory Records**
- One **Hospital** → Many **Ambulances**
- One **Ambulance** → Many **Bookings** (historically)

---

## 🏗 Design Principles

- Fully normalized relational schema
- Clear ownership of emergency requests
- Separation of transactional data (Bookings) from resource data (Beds & Ambulances)
- Scalable hospital and ambulance allocation structure
- Optional ambulance assignment per emergency request

This structure ensures data consistency, scalability, and efficient emergency response management.