import json
from typing import List

from apistar import App, Route, types, validators
from apistar.http import JSONResponse

NOT_FOUND = 'Sorry! Not found...'

def load_data():
	with open('ex_prisoners.json') as f:
		data = json.loads(f.read())
		return {item['username']: item for item in data}

data = load_data()

# Str to float 
for item in data.items():
	item[1]['latitude'] = float(item[1]['latitude'])
	item[1]['longitude'] = float(item[1]['longitude'])


class Prisoner(types.Type):
	bracelet_ip = validators.String(max_length=100)
	wanted = validators.Boolean(default=False)
	username = validators.String(max_length=30)
	latitude = validators.Number(maximum=90, minimum=-90)
	longitude = validators.Number(maximum=180, minimum=-180)

# API Methods

def list_prisoners():
	''' List all prisoners '''
	return [Prisoner(prisoner[1]) for prisoner in data.items()]


def get_prisoner(username):
	''' Returns JSON with specified prisoner '''
	if not data.get(username):
		return JSONResponse({'error': NOT_FOUND}, 404)
	return JSONResponse(data[username], 200)


def create_prisoner(prisoner: Prisoner) -> JSONResponse:
	''' Creates the specified prisoner ''' 
	if data.get(prisoner.username):
		return JSONResponse({'error': 'User already exists!'}, 400)

	data[prisoner.username] = prisoner
	return JSONResponse(Prisoner(prisoner), 200)


def update_prisoner(username: str, prisoner: Prisoner) -> JSONResponse:
	''' Updates the specified prisoner ''' 
	if not data.get(username):
		return JSONResponse({'error': NOT_FOUND}, 404)

	data[prisoner.id] = prisoner
	return JSONResponse(Prisoner(prisoner, 200))


def remove_prisoner(username):
	''' Deletes specified user '''
	if not data.get(username):
		return JSONResponse({'error': NOT_FOUND}, 404)

	del data[username]
	return JSONResponse({}, 204)



routes = [
	Route('/', method='GET', handler=list_prisoners),
	Route('/', method='POST', handler=create_prisoner),
	Route('/{username}/', method='GET', handler=get_prisoner),
	Route('/{username}/', method='PUT', handler=update_prisoner),
	Route('/{username}/', method='DELETE', handler=remove_prisoner),	
]

app = App(routes=routes)

if __name__ == '__main__':
	app.serve('localhost', 1234, debug=True)