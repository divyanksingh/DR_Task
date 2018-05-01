pip install -r requirements.txt
DIR=migrations
if [ ! -d $DIR ]
then
	flask db init
fi
flask db migrate
flask db upgrade
gunicorn application.init_app:app --daemon