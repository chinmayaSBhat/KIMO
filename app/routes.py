from fastapi import APIRouter

router = APIRouter()
# define the endpoint to get a list of all available courses
@router.get('/courses')
async def get_courses(sort_by: str = 'alphabetical', domain: str = None):
    return "here"
    if sort_by == 'alphabetical':
        sort_field = 'name'
        sort_order = 1
    elif sort_by == 'date':
        sort_field = 'date'
        sort_order = -1
    elif sort_by == 'rating':
        sort_field = 'total_rating'
        sort_order = -1
    else:
        return {'error': 'Invalid sort field'}

    query = {}
    if domain:
        query['domain'] = domain

    results = courses.find(query).sort(sort_field, sort_order)

    return {'courses': [result for result in results]}

# define the endpoint to get the course overview
@router.get('/courses/{course_id}')
async def get_course(course_id: str):
    result = courses.find_one({'_id': course_id})
    if result:
        return {'course': result}
    else:
        return {'error': 'Invalid course ID'}

# define the endpoint to get specific chapter information
@router.get('/courses/{course_id}/{chapter_id}')
async def get_chapter(course_id: str, chapter_id: str):
    result = courses.find_one({'_id': course_id})
    if result:
        chapters = result['chapters']
        for chapter in chapters:
            if chapter['title'] == chapter_id:
                return {'chapter': chapter}

        return {'error': 'Invalid chapter ID'}
    else:
        return {'error': 'Invalid course ID'}

# define the endpoint to allow users to rate each chapter
@router.post('/courses/{course_id}/{chapter_id}/rate')
async def rate_chapter(course_id: str, chapter_id: str, rating: int):
    result = courses.find_one({'_id': course_id})
    if result:
        chapter_data = None
        chapters = result['chapters']
        for chapter in chapters:
            if chapter['title'] == chapter_id:
                chapter_data = chapter
                break

        if chapter_data:
            chapter_data['ratings'].routerend(rating)
            total_rating = sum(chapter_data['ratings'])
            num_ratings = len(chapter_data['ratings'])
            average_rating = total_rating / num_ratings
            courses.update_one({'_id': course_id, 'chapters.title': chapter_id}, {'$set': {'chapters.$.ratings': chapter_data['ratings'], 'chapters.$.average_rating': average_rating}, '$inc': {'total_rating': rating, 'num_ratings': 1}})
            return {'success': True}
        else:
            return {'error': 'Invalid chapter ID'}
    else:
        return {'error': 'Invalid course ID'}

