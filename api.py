import json
from apistar import App, Route, types, validators
from apistar.http import JSONResponse

def load_data():
	with open('ex_prisoners.json') as f:
		data = json.loads(f.read())
		return {item['bracelet_ip']: item for item in data}

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

def list_prisoners():
	return [Prisoner(prisoner[1]) for prisoner in data.items()]


routes = [
	Route('/', method='GET', handler=list_prisoners),
]

app = App(routes=routes)

if __name__ == '__main__':
	app.serve('localhost', 1234, debug=True)