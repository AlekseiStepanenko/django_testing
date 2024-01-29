import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_course(client, course_factory):
    courses = course_factory(_quantity=10)
    course_id = courses[5].id
    url = f'/api/v1/courses/{course_id}/'
    response = client.get(url)
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == course_id


@pytest.mark.django_db
def test_get_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    response = client.get(f'/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_get_filter_id_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    course_id = courses[2].id
    url = f'/api/v1/courses/'
    response = client.get(url, data={'id': course_id})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['id'] == course_id


@pytest.mark.django_db
def test_get_filter_name_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    course_name = courses[2].name
    url = f'/api/v1/courses/'
    response = client.get(url, data={'name': course_name})
    data = response.json()
    assert response.status_code == 200
    assert data[0]['name'] == course_name


@pytest.mark.django_db
def test_post_create_courses(client):
    count = Course.objects.count()
    url = f'/api/v1/courses/'
    response = client.post(url, data={'name': 'Программирование'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1

@pytest.mark.django_db
def test_post_update_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    course_id = courses[2].id
    url = f'/api/v1/courses/'
    update_response = client.post(url, data={'id': course_id, 'name': 'Обновление'})
    assert update_response.status_code == 201
    url_course = f'/api/v1/courses/{course_id}/'
    response = client.get(url_course)
    data = response.json()
    assert data[0]['name'] == 'Обновление'


@pytest.mark.django_db
def test_post_delete_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    course_id = courses[2].id
    count = Course.objects.count()
    url = f'/api/v1/courses/{course_id}/'
    response = client.delete(url)
    assert response.status_code == 204
    assert Course.objects.count() == count - 1


