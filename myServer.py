from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
from facenet.src.myCompare import my_detect_face
import jsonpickle.ext.numpy as jsonpickle_numpy

jsonpickle_numpy.register_handlers()

# Initilize the Flask application
app = Flask(__name__)

def req2img(request):
    r = request
    # Convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # Decode image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return image

# Route HTTP posts to this method
@app.route('/test', methods=['POST'])
def test():
    """
    r = request
    # Convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # Decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    """
    img = req2img(request)

    # Build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}

    # Encode response using jsonpicke
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

# Simple health check
@app.route('/ping', methods=['GET'])
def ping():
    return 'pong\n'

# Face box
@app.route('/facebox', methods=['POST'])
def facebox():
    img = req2img(request) 

    # Do the face detection
    face_box = my_detect_face(img, 1)
    print(type(face_box))

     # Build a response dict to send back to client
    #response = {'box': '[{} {} {} {}]'.format()}

    # Encode response using jsonpicke
    # response_pickled = jsonpickle.encode(response)
    response_pickled = jsonpickle.encode(face_box)


    return Response(response=response_pickled, status=200, mimetype="application/json")

   
# Start Flask app
app.run(host="0.0.0.0", port=5000)
