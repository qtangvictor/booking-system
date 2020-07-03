# -*- coding: utf-8 -*-
# filename: index.wsgi
import sae
import web
from handle import Handle
from book import Book
from cancel import Cancel


urls = (
    '/wx', 'Handle',
    '/book', 'Book',
    '/cancel','Cancel',
)

app = web.application(urls, globals()).wsgifunc()
application = sae.create_wsgi_app(app)