from fastapi import FastAPI
from database import engine, Base
from controllers import sos_controller
from controllers import admin_controller

app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(sos_controller.router)
app.include_router(admin_controller.router)
@app.get("/")
def health_check():
    return {"status": "Backend Running"}

