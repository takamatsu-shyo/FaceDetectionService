from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2

# Initilize the Flask application
app = Flask(__name__)

# Route HTTP posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # Convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # Decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Do sth?

    # Build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}

    # Encode response using jsonpicke
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")
    
# Start Flask app
app.run(host="0.0.0.0", port=5000)
