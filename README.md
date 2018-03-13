# Shops

Here is a lovely little webapp that lists shops per the specification
at https://github.com/mattyg/web-coding-challenge

## How to run it

You'll need to have Python 3 installed, along with pip and virtualenv.

Assuming you have a directory at ~/.virtualenvs, you can then create a virtualenv for this app like so:
 
`python -m venv ~/.virtualenvs/shops`

After that, clone this repository and navigate to the directory you've saved it in, and run this:

`source ~/.virtualenvs/shops/bin/activate`

Before you run the app for the first time, you'll also need to run these in the very same shell session you just activated your virtualenv in:

`pip install django djangorestframework djet djoser`
`./manage.py migrate`

Having done that, run:

`./manage.py runserver`

Then, you should be able to navigate to http://localhost:8000/shops/
and see this lovely toy.
