# Udacity Full Stack Web Developer Nanodegree Capstone Project 

## UdaciMarket Management System
#
### Installing Dependencies

#### Python 3.7

Follow instructions to install Python 3.7 for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Running the app in an virtual environment is highly recommended. This keeps the dependencies for the project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the main directory (which is right under CAPSTONE_GROCERY_MARKET) and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we"ll use handle the lightweight sqlite database. You"ll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we"ll use to handle cross origin requests from our frontend server. 
  
- [Flask-Swagger-UI](https://github.com/swagger-api/swagger-ui) is a collection of HTML, JavaScript, and CSS assets that dynamically generate beautiful documentation from a Swagger-compliant API.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql grocery_market < grocery.psql
```

## Running the application

First ensure you are working using your created virtual environment; then to run the application, execute:

```bash
python app.py
```


## Endpoints

Endpoints information is documented via Swagger UI and can be accessed by appending `/swagger` to the host address.


## Error Handling

Errors are returned in their coressponding webpages:

The error codes currently used are:

* 400 – Bad Request
* 401 - Unauthorized
* 403 - Forbidden
* 404 – Not Found
* 405 - Method Not Allowed
* 422 – Unprocessable
* 500 – Something's Not Right

## Testing

To run the tests, run:
```
dropdb grocery_market_test
createdb grocery_market_test
psql grocery_market_test < grocery.sql
python test_flaskr.py
```