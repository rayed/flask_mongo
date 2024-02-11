

# Flask App with MongoDB Backend




## Installation

    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt

## Start MongoDB

    # NOTE: no presistant for data
    docker run --rm --name mongodb -p 27017:27017 mongodb/mongodb-community-server:6.0-ubi8
    # Set user name and password: -e MONGO_INITDB_ROOT_USERNAME=user -e MONGO_INITDB_ROOT_PASSWORD=pass

## Run 

    flask --app flaskr run --port 5001 --debug

    http://localhost:5001/


## User command

    # Create new user 
    flask --app flaskr users create newuser
    # Reset user password
    flask --app flaskr users reset newuser
