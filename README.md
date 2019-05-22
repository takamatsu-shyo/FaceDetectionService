# Face Detection Service 

## What is this

Flask based microservice for face detection based on facenet. The service only provide detected face boxes however face verification is also possible with small changes from here.

(The repository contains the facenet as a submodule)

## Development environment

This repository is developed with followings. 

AWS Instance: p2.xlarge  
AMI: Deep Learning Base AMI   
Trained model: 20180402-114759.zip (VGGFace2)

## How to run the service
0. (Optional) Prepare your AWS environment 
1. Set the virtualenv and activate
2. ```git clone``` this repository
3. Don't forget after cloning ```git submodule update --init```
4. ```pip3 install -r requirements.txt``` for this repository.
5. Make a symbolic link from ```myCompare.py``` with ``` ln -s ~/FaceDetectionService/myCompare.py ~/FaceDetectionService/facenet/src``` 
6. Run the server with ```python3 myServer.py```
7. (Optional) Try with a simple health check with ```curl localhost:5000/ping```
8. Prepare an image in ```./photo``` 
9. From another terminal, POST a photo with ```python3 myClient.py your_file.jpg -f``` . You may try it from same host or setup SSH portforwading. ```ssh -L localhost:5000:localhost:5000 ...```
10. You will receive image size and detected face box with JSON, for example ```{'message': 'image received. size=760x882'}```
```{'py/object': 'numpy.ndarray', 'values': [208, 130, 522, 547], 'dtype': 'int32'}```

## How to run the service by Docker
0. (Optional) Prepare your AWS environment 
1. Pull the image with ```docker pull tensorflow/tensorflow:latest-gpu```
2. Build an image ```docker build -t face/detect:1.0 .```
3. Run the image ```nvidia-docker run --rm -p 5000:5000/tcp face/detect:1.0```
4. Prepare an image in ```./photo``` 
5. From another terminal, POST a photo with ```python3 myClient.py your_file.jpg -f``` . You may try it from same host or setup SSH port forwading. ```ssh -L localhost:5000:localhost:5000 ...```
6. You will receive image size and detected face box with JSON, for example ```{'message': 'image received. size=760x882'} ```
```{'py/object': 'numpy.ndarray', 'values': [208, 130, 522, 547], 'dtype': 'int32'}```

## References

### Flask sample code (tranfser JPEG image)
 <https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594>

### How to setup AWS Deep learning AMI
<https://aws.amazon.com/blogs/machine-learning/get-started-with-deep-learning-using-the-aws-deep-learning-ami/>

### GPU supported Docker image from Tensorflow
<https://www.tensorflow.org/install/docker#gpu_support>