# ! /bin/sh

echo "=========================================================="
echo "                 This is for testing."
echo "----------------------------------------------------------"
if [ -d ".env" ];
then
    echo "Enabling virtual env"
else
    echo "No Virtual env. Please run setup.sh first"
    exit N
fi

# Activate virtual env
. .env/bin/activate
export ENV=testing

pytest --verbose --disable-warnings -s

# coverage run -m pytest --verbose --disable-warnings -s
# coverage report -m

deactivate