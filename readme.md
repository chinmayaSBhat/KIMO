**Technologies Used**
Python
FastAPI (a modern web framework)
MongoDB (a NoSQL database)
Pydantic (for data validation)
Pytest (for testing)

**Installation**
Once you download and extract the files, navigate the folder.

```python
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

then,
```console
pip install -r requirements.txt
```

Assuming you have mongodb installed,

open insert_to_mongo.py file and update the connection details if required,
then,

```console
python insert_to_mongo.py
```

Run the app:
```console
uvicorn app.main:app --reload
```

The app should now be running locally at http://127.0.0.1:8000/. You can test the API endpoints using a tool like curl or a web browser, or by using a REST client like Postman 


**API Endpoints**
The app provides the following API endpoints:


GET /courses: Get a list of all courses
GET /courses/{course_id}: Get details of a specific course
GET /courses/{course_id}/chapter/{chapter_name}: Get details of a specific chapter of a course
POST /courses/{course_id}/chapter/{chapter_name}/rating: post rating for a specific chapter of a course

**Testing**

To run the tests, update the course id, chapter name in the DB and run,

```console
pytest test_routes.py
```

