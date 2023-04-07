import json
from fastapi.testclient import TestClient

# Import  FastAPI app instance from  main.py file
from main import app

# Create a test client for making HTTP requests
client = TestClient(app)

# Test get_courses() endpoint with sort by date
def test_get_courses_sortby_date():
    response = client.get("/courses/", params={"sort_by": 'date'})
    assert response.status_code == 200
    

# Test get_courses() endpoint with sort by default, alphabetically
def test_get_courses_sort_by_alphabetics():
    response = client.get("/courses/")
    assert response.status_code == 200
    


# Test get_course() endpoint
def test_get_course():
    
    response = client.get("/courses/643027bac9ad9c25751da07e")
    assert response.status_code == 200
    

# Test get_chapter() endpoint
def test_get_chapter():
    
    response = client.get("/courses/643027bac9ad9c25751da07e/chapter/Introduction to Convolutional Neural Networks for Visual Recognition")
    assert response.status_code == 200
    

# Test rate_chapter() endpoint
def test_rate_chapter():
    # Create a TestClient instance
    client = TestClient(app)

    # Define the test data
    course_id = "643027bac9ad9c25751da07e"  # Replace with valid course ID from  database
    chapter_name = "Introduction to Convolutional Neural Networks for Visual Recognition"  # Replace with valid chapter name from  database
    rating = 1

    # Send a POST request to the rate_chapter API endpoint
    response = client.post(f"/courses/{course_id}/chapter/{chapter_name}/rate", params={"rating": rating})

    # Assert the response status code is 200 (OK)
    assert response.status_code == 200

    assert response.json() == {"message": "Chapter rated successfully"}
