from fastapi import FastAPI
from .routers import calendar, curriculum, timetable
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # The origin of your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calendar.router, prefix="/calendar", tags=["Calendar"])
app.include_router(curriculum.router, prefix="/curriculum", tags=["Curriculum"])
app.include_router(timetable.router, prefix="/timetable", tags=["Timetable"])
app.include_router(timetable.router, prefix="/timetable", tags=["Timetable"])