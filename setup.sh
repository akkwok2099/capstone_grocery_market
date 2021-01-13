#!/bin/bash

# ************************************************************* #
# *                                                           * #
# * This script will create the virtual environment, generate * #
# * .env file (configuration), install dependencies in the    * #
# * virtual environment, and do the initial setup of the two  * #
# * database for you. Before proceeding, please make sure     * #
# * that Python 3.7 is installed on your machine. And please  * #
# * remember to put down your database password in .env       * #
# *                                                           * #
# ************************************************************* #

# Create virtual environment
echo "Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "INFO: .venv directory already exist! Skipping..."
else
    python -m venv .venv
fi
echo "Virutal environment created"

# Rename .env-local file to .env in root
echo "Generating .env file..."
if [ -f ".env" ]; then
  echo "INFO: .env file already exist! Skipping..."
else
  mv .env-local .env
fi
echo ".env file created"

sleep 4

# Activate virtual environment
source .venv/Scripts/activate

# Update pip before installing dependencies
echo "Installing dependecies..."
python -m pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencies installed"

sleep 4

# Setup database and test database for project
echo "Setting up application database..."
createdb -Upostgres grocery_market
psql -Upostgres grocery_market < grocery.sql
echo "Application database initialization completed"

echo "Setting up test database..."
createdb -Upostgres grocery_market_test
psql -Upostgres grocery_market_test < grocery.sql
echo "Test database initialization completed"

# Setup Auth0 process constants
echo "Setting up environmental variables..."
export AUTH0_DOMAIN=skittishloki.auth0.com
export ALGORITHMS=['RS256']
export CLIENT_ID=Cu7QnsZ3tBNp8HMjfcMntZ1KKZQi03An
export CLIENT_SECRET=oeMgHc0KlMv7Q3h6knz6PeJBxy1FAiSRyUEMNK719IZp3w-E5Yrw4BbtrOushmEi
export API_AUDIENCE=http://localhost:8181
export ACCESS_TOKEN_URL=https://skittishloki.auth0.com/oauth/token
export AUTHORIZE_URL=https://skittishloki.auth0.com/authorize
export CALLBACK_URL=http://localhost:8181/callback
export SECRET_KEY=WeDidntStarttheFire
echo "Environmental variables created"
echo "*** Application setup process completed ***"

# Run flask server
# python app.py