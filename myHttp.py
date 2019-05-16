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

class HttpService:
    name = "http_service"

    @http('GET', '/get/<int:value>')
    def get_method(self, request, value):
        return json.dumps({'value': value})

    @http('POST', '/post')
    def do_post(self, request):

        """
        print("Request", request)
        r = request

        # convert string of image data to uint8
        nparr = np.fromstring(r.data, np.uint8)
        print("nparr", nparr)

        # decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print("after decode", img.size)
        """ 

        return u"received: {}".format(request.get_data(as_text=True))
        #return img.size

    @http('GET,PUT,POST,DELETE', '/multi')
    def do_multi(self, request):
        return request.method

