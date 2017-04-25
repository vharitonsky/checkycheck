# things.py

# Let's get this party started!
import os
import falcon
from pymongo import MongoClient


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
mclient = MongoClient(os.environ['MONGODB_URI'])

class AddResource(object):
    def on_add(self, req, resp):
        db = mclient['test-database']
        db.counter.insert({})
        resp.status = falcon.HTTP_200
        resp.body = str(db.counter.count())

class ThingsResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = ('\nTwo things awe me most, the starry sky '
                     'above me and the moral law within me.\n'
                     '\n'
                     '    ~ Immanuel Kant\n\n')

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()
add = AddResource()

# things will handle all requests to the '/things' URL path
app.add_route('/add', add)
app.add_route('/things', things)
