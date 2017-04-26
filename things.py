# things.py

# Let's get this party started!
import os
import falcon
import re
import logging
from pymongo import MongoClient


log = logging.getLogger(__name__)

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
db = MongoClient(os.environ['MONGODB_URI'])[os.environ['MONGODB_URI'].split('/')[-1]]


class CheckResource(object):

    def get_page(self, req):
        page = req.get_param('page')
        clean_page = re.sub('[^a-zA-z]', '', page) + '.html'
        log.info(clean_page)
        return clean_page

    def on_get(self, req, resp):
        clean_page = self.get_page(req)

        if os.path.exists(clean_page):
            resp.status = falcon.HTTP_200
            resp.body = open(clean_page).read()
            resp.body.replace('</html>', (
                '<head> '
                '<script type="text/javascript">%s</script>'
                '</head>'
                '</html>' % open('controls.js').read()
            ))
            resp.content_type = 'text/html'
        else:
            resp.status = falcon.HTTP_404
            resp.body = "Not found"

    def on_post(self, req, resp):
        clean_page = self.get_page(req)
        product_id = req.get_param('product_id')
        computer = req.get_param('comp')
        moderator = req.get_param('moderator')
        db.checks.replaceOne({
            'product_id': product_id
        }, {'product_id': product_id,
            'computer': computer, 
            'moderator': moderator,
            'page': clean_page,
        })
        resp.status = falcon.HTTP_200
        resp.body = 'OK'


class AddResource(object):

    def on_get(self, req, resp):
        db.counter.insert({})
        resp.status = falcon.HTTP_200
        resp.body = str(db.counter.count())


# falcon.API instances are callable WSGI apps
app = falcon.API()
app.req_options.auto_parse_form_urlencoded = True

# Resources are represented by long-lived class instances
add = AddResource()
check = CheckResource()

# things will handle all requests to the '/things' URL path
app.add_route('/add', add)
app.add_route('/check', check)