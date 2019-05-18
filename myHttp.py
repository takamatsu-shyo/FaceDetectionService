# Flask sample
# https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594

# Nameko sample
# myHttp.py
# https://docs.nameko.io/en/stable/built_in_extensions.html#http

# Decode jpeg to cv2
# https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594

# validate_jpeg
# https://www.programcreek.com/python/example/60711/flask.request.data

import json
from nameko.web.handlers import http
import jsonpickle
import numpy as np
import cv2
import logging

class HttpService:
    name = "http_service"

    @http('GET', '/ping')
    def get_ping(self, request):
        return json.dumps({'ping': 'pong'})

    @http('GET', '/get/<int:value>')
    def get_method(self, request, value):
        return json.dumps({'value': value})

    @http('POST', '/test')
    def do_test(self, request):
        # Convert then decode
        r = request
        nparr = np.fromstring(r.data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Do your job here!

        # Response
        response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}
        response_pickled = jsonpickle.encode(response)

        return response_pickled

    @http('POST', '/post')
    def do_post(self, request):
        return u"received: {}".format(request.get_data(as_text=True))

    @http('GET,PUT,POST,DELETE', '/multi')
    def do_multi(self, request):
        return request.method

