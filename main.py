from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from bson import ObjectId
from typing import List
from app import crud, schemas

# Create FastAPI app
app = FastAPI()

# Connect to MongoDB
mongo_client = MongoClient("mongodb://127.0.0.1:27017/")  # Update the MongoDB connection string if needed
db = mongo_client["kimo"]  
collection = db["courses"]

# API endpoints

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.get("/courses/", response_model=List[schemas.Course], tags=["Courses"])
async def get_courses(
    sort_by: str = "alphabetical",
    domain: str = None,
):
    """
    Get list of all available courses with optional sorting by title, date, or rating.
    """
    if sort_by not in ["alphabetical", "date", "rating"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by parameter")

    courses = crud.get_all_courses(collection)
    print(courses)
    if sort_by == "alphabetical":
        courses.sort(key=lambda x: x["name"])
    elif sort_by == "date":
        courses.sort(key=lambda x: x["date"], reverse=True)
    elif sort_by == "rating":
        courses.sort(key=lambda x: x["rating"], reverse=True)

    return courses

@app.get("/courses/{course_id}", response_model=schemas.Course, tags=["Courses"])
async def get_course(course_id: str):
    """
    Get course overview by course_id.
    """
    course = crud.get_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@app.get("/courses/{course_id}/chapter/{chapter_name}", response_model=schemas.Chapter, tags=["Courses"])
async def get_chapter(course_id: str, chapter_name: str):
    """
    Get chapter information by course_id and chapter_name.
    """
    chapter = crud.get_chapter(course_id, chapter_name)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@app.post("/courses/{course_id}/chapter/{chapter_name}/rate", tags=["Courses"])
async def rate_chapter(course_id: str, chapter_name: str, rating: int):
    """
    Rate a chapter (positive/negative) by course_id and chapter_name.
    """
    if rating not in [1, -1]:
        raise HTTPException(status_code=400, detail="Invalid rating value")

    crud.rate_chapter(course_id, chapter_name, rating)

    return {"message": "Chapter rated successfully"}

