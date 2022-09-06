un#! /bin/sh
echo "-----Local Run-----"
if [ -d ".env" ];
then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run setup.sh first"
    exit N
fi

# Activate virtual env
. .env/bin/activate
export ENV=development
# gunicorn main:app --worker-class gevent --bind 127.0.0.1:8080 --workers=4
gunicorn main:app --worker-class gevent --bind 127.0.0.1:8000
deactivate