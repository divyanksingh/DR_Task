from rest.restfull import Resource


class BaseBlog(Resource):
	GET_URL_LIST = ['/blog', '/blog/<int:id>']
	POST_URL_LIST = ['/blog/']
	PUT_URL_LIST = ['/blog/<int:id>']
	DELETE_URL_LIST = ['/blog/<int:id>']
	AUTH_REQUIRED = ['GET', 'POST', 'PUT', 'DELETE']

