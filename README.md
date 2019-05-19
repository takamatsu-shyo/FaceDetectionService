# FaceDetectionService 

## What is this

Flask based microservice for face detection based on facenet. The service only provide detected face boxes however face verification is also possible with small changes from here.

(The repository contains the facenet as a submodule)

## Development environment

This repository is developed with followings. 

AWS Instance: p2.xlarge  
AMI: Deep Learning Base AMI   
Trained model: 20180402-114759.zip (VGGFace2)

## How to run the service (step-by-step)

0. (Optional) Prepaire your AWS environment 
1. Set the virtualenv and activate
2. ```git clone``` this repository
3. Don't foreget after clonining ```git submodule update --init```
4. ```pip3 install -r requirements.txt``` for this repository and also for facenet
5. Make a symbolic link from ```myCompare.py``` with ``` ln -s ~/FaceDetectionService/myCompare.py ~/FaceDetectionService/facenet/src``` 
6. Prepair an image in ```./photo``` and edit file name in ```client.py```
7. Run the server with ```python3 myServer.py```
8. (Optional) Try with a simple health check with ```curl localhost:5000/ping```
9. From another terminal, POST a photo with ```python3 client.py```. You may try ```tmux``` for multiple terminal with a SSH session.
10. You will receive a detected face box with JSON, for example ```{'values': [[-4, 74, 240, 383], [286, 71, 521, 387], [559, 88, 796, 388]], 'dtype': 'int32', 'py/object': 'numpy.ndarray'}```

## TODO
- nvidia-docker
- Performance
- CLI
- CI
- Error handling
- Logging

## References

### Flask sample code (tranfser JPEG image)
 <https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594>

### How to setup AWS Deep learning AMI
<https://aws.amazon.com/blogs/machine-learning/get-started-with-deep-learning-using-the-aws-deep-learning-ami/>