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
RUN rm facenet/src/myCompare.py
RUN cp myCompare.py facenet/src

# This is just information!
# Don't forget "-p 5000:5000/tcp" when you run the image
EXPOSE 5000/tcp
CMD ["python", "myServer.py"]
