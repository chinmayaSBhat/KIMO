from typing import List, Optional
from pymongo import MongoClient
from bson.objectid import ObjectId
from fastapi import HTTPException

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["kimo"]
courses_collection = db["courses"]

# CRUD operations

def get_all_courses(sort_by: str = 'name', domain: Optional[str] = None) -> List[dict]:
    """
    Get all courses with optional sorting and domain filtering
    """
    # Prepare sort query
    sort_query = {'name': 1}  # default sorting by name ascending
    if sort_by == 'date':
        sort_query = {'date': -1}  # sorting by date descending
    elif sort_by == 'rating':
        sort_query = {'rating': -1}  # sorting by rating descending

    # Prepare filter query
    filter_query = {}
    if domain:
        filter_query = {'domain': domain}

    # Fetch courses from MongoDB
    courses = list(courses_collection.find(filter_query).sort(list(sort_query.items())))

    return courses

def get_course(course_id: str) -> dict:
    """
    Get course details by course ID
    """
    course = courses_collection.find_one({'_id': ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

def get_chapter(course_id: str, chapter_name: str) -> dict:
    """
    Get chapter details by course ID and chapter ID
    """
    course = courses_collection.find_one({'_id': ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    chapter = next((c for c in course['chapters'] if str(c['name']) == chapter_name), None)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")

    return chapter

def rate_chapter(course_id: str, chapter_name: str, rating: int) -> dict:
    """
    Rate a chapter in a course
    """
    course = courses_collection.find_one({'_id': ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    chapter = next((c for c in course['chapters'] if str(c['name']) == chapter_name), None)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    if 'ratings' not in chapter:
        chapter['ratings'] = []

    chapter['ratings'].append(rating)
    chapter['rating'] = sum(chapter['ratings']) / len(chapter['ratings'])

    courses_collection.update_one({'_id': ObjectId(course_id)}, {'$set': {'chapters': course['chapters']}})

    return chapter

