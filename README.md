Database as a Service (DBaas)
===================================

Introduction
============

This is an implementation of a database as service api written in python + django. We will try to follow some hypermedia concepts throughout the api calls.

Initially we will only support MongoDB.

Status
=======

In development (alpha)

Setup your local environment
============================

    mkvirtualenv dbaas
    workon dbaas
    
    
You will also need to create a sitecustomize.py file with the following content in 
yours python's lib directory.

    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")

Then, finally

    make check_environment
    
Install the required python packages.

    make pip
    
Create the tables structure (see the next item)

## DB

We will be using simple-db-migrate to maintain the migrations used by the project. However, for now, you can
just run syncdb to create the table structures. There is a make shortcut to help you with that

    make db_drop_and_create

## Running the project

    make run
    
Point your browser to http://localhost:8000/admin/

