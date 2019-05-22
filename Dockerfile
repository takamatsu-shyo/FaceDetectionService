FROM tensorflow/tensorflow:latest-gpu

# Nvidia docker image has an issue
# https://github.com/NVIDIA/nvidia-docker/issues/864
#
# >>> import cv2 
#Traceback (most recent call last):
#  File "<stdin>", line 1, in <module>
#  File "/usr/local/lib/python2.7/dist-packages/cv2/__init__.py", line 3, in <module> 
#    from .cv2 import *
#ImportError: libSM.so.6: cannot open shared object file: No such file or directory
RUN apt-get update
RUN apt-get install -y libsm6 libxext6 libxrender-dev

# Install dependency
RUN mkdir facedetect
WORKDIR /facedetect
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Overwrite symblic link of myCompare
RUN rm facenet/src/myCompare_2.py
RUN cp myCompare_2.py facenet/src

# One more file to overwrite so that we can avoid "allow_pickle=True" issue
# BUT! NumPy 1.16.0 and earlier allow remote code execution.
# Thus for production environment it is good to take other solutions.
# https://nvd.nist.gov/vuln/detail/CVE-2019-6446
RUN cp myDetect_face_2.py facenet/src/align/detect_face.py

# This is just information!
# Don't forget "-p 5000:5000/tcp" when you run the image
EXPOSE 5000/tcp
CMD ["python", "myServer_2.py"]
