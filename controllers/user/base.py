from rest.restfull import Resource


class BaseUserCrud(Resource):
	GET_URL_LIST = ['/user/', '/user/<int:id>']
	POST_URL_LIST = ['/user/']
	PUT_URL_LIST = ['/user/<int:id>']
	DELETE_URL_LIST = ['/user/<int:id>']
	AUTH_REQUIRED = ['GET', 'PUT', 'DELETE']

class BaseUserLogin(Resource):
	POST_URL_LIST = ['/login']
	AUTH_REQUIRED = []



