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
if [ -d ".venv" ]; then
    echo "INFO: .venv directory already exist! Skipping..."
else
    python -m venv .venv
fi

# Rename .env-local file to .env in root
if [ -f ".env" ]; then
  echo "INFO: .env file already exist! Skipping..."
else
  mv .env-local .env
fi

sleep 3

# Activate virtual environment
source .venv/Scripts/activate

# Update pip before installing dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

sleep 3

# Setup database and test database for project
createdb -Upostgres grocery_market
psql -Upostgres grocery_market < grocery.sql

createdb -Upostgres grocery_market_test
psql -Upostgres grocery_market_test < grocery.sql

# Run flask server
# python app.py