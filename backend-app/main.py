from fastapi import FastAPI
from database import Base,engine
from controllers import sos_controller,admin_controller
from models import user,hospital,booking, bed, ambulance
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(sos_controller.router)
app.include_router(admin_controller.router)
@app.get("/")
def health_check():
    return {"status": "Backend Running"}

