# things.py

# Let's get this party started!
import os
import falcon
import re
from pymongo import MongoClient


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
db = MongoClient(os.environ['MONGODB_URI'])[os.environ['MONGODB_URI'].split('/')[-1]]

class CheckResource(object):

    def get_page(self, req):
       page = req.get_param('page')
       clean_page = re.replace('^[a-zA-z]', '', page) + '.html'
       return page
 

    def on_get(self, req, resp):
       clean_page = self.get_page(req)

       if os.path.exists(clean_page):        
           resp.status = falcon.HTTP_200
           resp.body = open(clean_page).read()
       else:
           resp.status = falcon.HTTP_404
           resp.body = "Not found"

    def on_post(self, req, resp):
        clean_page = self.get_page(req)
        
       


class AddResource(object):
    def on_get(self, req, resp):
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
