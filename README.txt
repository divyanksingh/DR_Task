Create a virtual environment and activate it.

Run the quick_start script
./quick_start.sh




GET 	/v1/user/	
	Returns a list of all the users

GET 	/v1/user/<int:id>
	Returns the user with user.id equal to parameter id

POST 	/v1/user/
	Add a new user
		Body: {"username": <String: required>,
				"display_name": <String>,
				"password": <String: required>
				}

PUT 	/v1/user/<int:id>
	Update the user with user.id equal to parameter id
		Body: {"display_name": <String>,
				"password": <String>
				}

DELETE 	/v1/user/<int:id>
	Delete user with user.id equal to parameter id

POST 	/v1/login
	Login user and return auth_token
		Body: {
				"username": <String: required>,
				"password": <String: required>
			}

GET 	/v1/blog
	Return a blog_list based on query parameters
		Query parameters: {
			"refresh": <Boolean>,
			"max_id": <int: smallest blog_id present in client cache>,
			"since_id": <int: largest blog_id present in client cache>,
			"last_updated": <string(yyyy-mm-dd hh:mm:ss): latest update time among all the blogs in the cache>
		}
		if refresh is true, max_id, since_id and last_updated should be provided
		if no parameter is provided, latest n blogs are returned where n is per_page_count
		if only max_id is provided, n blogs before max_id are returned


GET 	/v1/blog/<int:id>
	Return blog with blog.id equal to parameter id

POST 	/v1/blog/
	Add a new blog
		Body: {
				"title": <String: required>,
				"description": <String>
			}

PUT 	/v1/blog/<int:id>
	Update a blog with blog.id equal to id

DELETE 	/v1/blog/<int:id>
	Soft delete a blog with blog.id equal to id