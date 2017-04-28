# things.py

# Let's get this party started!
import os
import falcon
import re
import logging
from pymongo import MongoClient, ASCENDING, DESCENDING


log = logging.getLogger(__name__)

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
db = MongoClient(os.environ['MONGODB_URI'])[os.environ['MONGODB_URI'].split('/')[-1]]


def get_page(req):
    page = req.get_param('page')
    clean_page = re.sub('[^a-zA-z]', '', page) + '.html'
    log.info(clean_page)
    return clean_page


class ShowResource(object):

    def on_get(self, req, resp):
        clean_page = get_page(req)
        total = db.checks.find({
            'page': '^%s' % clean_page,
        }).count() or 1
        # db.checks.create_index(
        #     ['computer', ASCENDING],
        #     ['moderator', DESCENDING]
        # )
        false_positive = db.checks.find({
            'page': '^%s' % clean_page,
            'computer': True,
            'moderator': False,
        }).count()
        false_negative = db.checks.find({
            'page': '^%s' % clean_page,
            'computer': False,
            'moderator': False,
        }).count()
        accuracy = float(total - (false_positive + false_negative))/total * 100
        resp.status = falcon.HTTP_404
        resp.body = """
            Total: %s
            False Positive: %s
            False Negative: %s
            Accuracy: %s
        """ % (total, false_positive, false_negative, accuracy)


class CheckResource(object):

    def on_get(self, req, resp):
        clean_page = get_page(req)

        if os.path.exists(clean_page):
            resp.status = falcon.HTTP_200
            resp.body = open(clean_page).read().replace('<html>', (
                '<html>'
                '<head> '
                '<script type="text/javascript">%s</script>'
                '</head>' % open('controls.js').read()
            ))
            resp.content_type = 'text/html'
        else:
            resp.status = falcon.HTTP_404
            resp.body = "Not found"

    def on_post(self, req, resp):
        clean_page = get_page(req)
        product_id = req.get_param('product_id')
        computer = bool(req.get_param('computer'))
        moderator = bool(req.get_param('moderator'))
        # db.checks.create_index('product_id')
        db.checks.replace_one({
            'product_id': product_id
        }, {'product_id': product_id,
            'computer': computer, 
            'moderator': moderator,
            'page': clean_page,
        }, upsert=True)
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
show = ShowResource()

# things will handle all requests to the '/things' URL path
app.add_route('/add', add)
app.add_route('/check', check)
app.add_route('/show', show)
