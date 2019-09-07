from apistar import test
from api import app, data, NOT_FOUND

client = test.TestClient(app)


def test_list_prisoners():
    '''  Testing API Method "list_prisoners" '''
    response = client.get('/')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1000
    assert type(data) == list
    prisoner = data[0]
    expected = {
        "bracelet_ip": "f395:5655:f1bb:5cb1:ab00:a63a:abc:aae6/56",
        "wanted": False,
        "username": "dilymanov0",
        "latitude": 45.697904,
        "longitude": 0.964671
    }
    assert prisoner == expected
    last_username = data[-1]['username']
    assert last_username == 'lnoddlesrr'


def test_get_prisoner():
    '''  Testing API Method "get_prisoner" '''
    response = client.get('/rtremmelrp')

    assert response.status_code == 200
    response = response.json()
    assert type(response) == dict
    expected = {
        "bracelet_ip": "a456:b93a:b9c5:e286:2c96:671f:430b:a52e/26",
        "username": "rtremmelrp",
        "wanted": False,
        "latitude": 48.8693156,
        "longitude": 2.3501981
    }
    assert response == expected


def test_get_prisoner_404():
    '''  Testing API Method "get_prisoner" '''
    response = client.get('/unexistingUsername')

    assert response.status_code == 404
    assert response.json() == {'error': NOT_FOUND}


def test_create_prisoner():
    '''  Testing API Method "create_prisoner" '''
    params = {
        'username': 'newUser',
        'bracelet_ip': 'a456:b93a:b9c5:e286:2sa6:671f:430b:a52e/26',
        'wanted': False,
        'latitude': 42,
        'longitude': 42
    }
    response = client.post('/', data=params)
    assert response.status_code == 200
    assert len(data) == 1001

    response = client.get('/newUser')
    assert response.status_code == 200
    expected = {
        'username': 'newUser',
        'bracelet_ip': 'a456:b93a:b9c5:e286:2sa6:671f:430b:a52e/26',
        'wanted': False,
        'latitude': 42,
        'longitude': 42
    }
    assert response.json() == expected


def test_create_prisoner_missing_data():
    '''  Testing API Method "create_prisoner" '''
    params = {'insufficient': 0}
    response = client.post('/', data=params)

    assert response.status_code == 400
    response = response.json()
    assert response['bracelet_ip'] == "The \"bracelet_ip\" field is required."
    assert response['username'] == "The \"username\" field is required."
    assert response['latitude'] == "The \"latitude\" field is required."
    assert response['longitude'] == "The \"longitude\" field is required."


def test_create_prisoner_validation():
    '''  Testing API Method "create_prisoner" '''
    params = {
        'username': 'A' * 50,
        'bracelet_ip': 'B' * 120,
        'wanted': 'notBool',
        'latitude': 200,
        'longitude': -200
    }
    response = client.post('/', data=params)

    assert response.status_code == 400
    response = response.json()
    assert response['bracelet_ip'] == "Must have no more than 100 characters."
    assert response['wanted'] == "Must be a valid boolean."
    assert response['username'] == "Must have no more than 30 characters."
    assert response['latitude'] == "Must be less than or equal to 90."
    assert response['longitude'] == "Must be greater than or equal to -180."


def test_update_prisoner():
    '''  Testing API Method "update_prisoner" '''
    params = {
        'username': 'gdivers2',
        'bracelet_ip': 'nweIp',
        'wanted': False,
        'latitude': 27,
        'longitude': -27
    }
    response = client.put('/gdivers2/', data=params)

    assert response.status_code == 200
    expected = {
        'username': 'gdivers2',
        'bracelet_ip': 'nweIp',
        'wanted': False,
        'latitude': 27,
        'longitude': -27
    }
    assert response.json() == expected
    response = client.get('/gdivers2')
    assert response.json() == expected


def test_update_prisoner_404():
    '''  Testing API Method "update_prisoner" '''
    params = {
        'username': 'unexistingUsername',
        'bracelet_ip': 'nweIp',
        'wanted': False,
        'latitude': 27,
        'longitude': -27
    }
    response = client.put('/unexistingUsername/', data=params)
    assert response.status_code == 404
    assert response.json() == {'error': NOT_FOUND}


def test_update_prisoner_missing_data():
    '''  Testing API Method "update_prisoner" '''
    params = {'insufficient': 0}
    response = client.put('/unexistingUsername/', data=params)
    assert response.status_code == 400
    response = response.json()
    assert response['bracelet_ip'] == "The \"bracelet_ip\" field is required."
    assert response['username'] == "The \"username\" field is required."
    assert response['latitude'] == "The \"latitude\" field is required."
    assert response['longitude'] == "The \"longitude\" field is required."


def test_update_prisoner_validation():
    '''  Testing API Method "update_prisoner" '''
    params = {
        'username': 'A' * 50,
        'bracelet_ip': 'B' * 120,
        'wanted': 'notBool',
        'latitude': 200,
        'longitude': -200
    }
    response = client.put('/unexistingUsername/', data=params)
    assert response.status_code == 400
    response = response.json()
    assert response['bracelet_ip'] == "Must have no more than 100 characters."
    assert response['wanted'] == "Must be a valid boolean."
    assert response['username'] == "Must have no more than 30 characters."
    assert response['latitude'] == "Must be less than or equal to 90."
    assert response['longitude'] == "Must be greater than or equal to -180."


def test_remove_prisoner():
    '''  Testing API Method "remove_prisoner" '''
    response = client.delete('/yburde4/')
    assert response.status_code == 204
    response = client.get('/yburde4/')
    assert response.status_code == 404


def test_remove_prisoner_404():
    '''  Testing API Method "remove_prisoner" '''
    response = client.delete('/unexistingUsername/')
    assert response.status_code == 404
    assert response.json() == {'error': NOT_FOUND}