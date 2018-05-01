pip install -r requirements.txt
export FLASK_CONFIG=test
export FLASK_APP=run.py
DIR=migrations
if [ ! -d $DIR ]
then
	flask db init
fi
flask db migrate
flask db upgrade
gunicorn application.init_app:app --daemon