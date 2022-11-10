# What are the odds ? - developer test

This project consists of a Django web application and a CLI which solve this 
[developer test](https://github.com/lioncowlionant/developer-test).

## Requirements

For reproductibility purposes, we advise to install the project in a dedicated 
virtual environment to make sure the specific requirements are satisfied. 
Recommended Python version: 3.8.x.

To install requirements:

```
pip install -r requirements.txt
```

## Django web application

To run in developer mode the web application, do

```
cd falconroute
python manage.py runserver
```

## CLI

To use the CLI, give as arguments to the script ``give-me-the-odds.sh`` paths 
to the millenium-falcon and empire files, for example

```
./give-me-the-odds.sh examples/example1/millennium-falcon.json examples/example1/empire.json
```





