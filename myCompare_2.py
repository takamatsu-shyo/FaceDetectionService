"""Modified for Face box"""

"""Performs face alignment and calculates L2 distance between the embeddings of images."""

# MIT License
# 
# Copyright (c) 2016 David Sandberg
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# Those __future__ lines should be the first otherwise SyntaxError
# Copied to myServer.py
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
"""

from scipy import misc
import tensorflow as tf
import numpy as np
import sys
import os
import copy
import argparse
import facenet
import align.detect_face
#import facenet.src.align.detect_face
#import src.align.detect_face
import time
           
# for Python2
sys.path.append('/facenet/src/align')
#import detect_face
#
# Dirty copy&paste from load_and_align_data (next one)            
#
#def load_and_face_box(image_paths, image_size, margin, gpu_memory_fraction):
def my_detect_face(img, loop):
    minsize = 20 # minimum size of face
    threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
    factor = 0.709 # scale factor
    gpu_memory_fraction = 0.9 # Quick dirty solution
    margin = 44		      # Quick dirty solution2

    # For performance testing
    print("Will be loop {0} times".format(loop))
    loop += 1
    
    print('Creating networks and loading parameters')
    start = time.time()
    for i in range(0,loop):
         with tf.Graph().as_default():
             gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
             sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
             with sess.as_default():
                 pnet, rnet, onet = facenet.src.align.detect_face.create_mtcnn(sess, None)
    elapsed_time_nw = time.time() - start
 
    # tmp_image_paths=copy.copy(image_paths)
    # img_list = []
    # for image in tmp_image_paths:
    # img = misc.imread(os.path.expanduser(image), mode='RGB')
    start = time.time()
    for i in range(0,loop):
        img_size = np.asarray(img.shape)[0:2]
    elapsed_time_asarray = time.time() - start

    start = time.time()
    for i in range(0,loop):
        bounding_boxes, _ = facenet.src.align.detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
    elapsed_time_bbox = time.time() - start

    if len(bounding_boxes) < 1:
      image_paths.remove(image)
      print("can't detect face, remove ", image)
      # continue
    """    
    det = np.squeeze(bounding_boxes[0,0:4])
    bb = np.zeros(4, dtype=np.int32)
    bb[0] = np.maximum(det[0]-margin/2, 0)
    bb[1] = np.maximum(det[1]-margin/2, 0)
    bb[2] = np.minimum(det[2]+margin/2, img_size[1])
    bb[3] = np.minimum(det[3]+margin/2, img_size[0])
    """
    # All detected face boxes
    start = time.time()
    det = np.squeeze(bounding_boxes[:,0:4]).astype(np.int32)
    elapsed_time_squeeze = time.time() - start

    print ("elapsed_time for Create NW: {0:.4f}".format(elapsed_time_nw) + "[sec]")
    print ("elapsed_time for asarray  : {0:.4f}".format(elapsed_time_asarray) + "[sec]")
    print ("elapsed_time for Detect   : {0:.4f}".format(elapsed_time_bbox) + "[sec]")
    print ("elapsed_time for squeeze  : {0:.4f}".format(elapsed_time_squeeze) + "[sec]")


    return det
           
def load_and_align_data(image_paths, image_size, margin, gpu_memory_fraction):

    minsize = 20 # minimum size of face
    threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
    factor = 0.709 # scale factor
    
    print('Creating networks and loading parameters')
    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = align.detect_face.create_mtcnn(sess, None)
  
    tmp_image_paths=copy.copy(image_paths)
    img_list = []
    for image in tmp_image_paths:
        img = misc.imread(os.path.expanduser(image), mode='RGB')
        img_size = np.asarray(img.shape)[0:2]
        bounding_boxes, _ = align.detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
        if len(bounding_boxes) < 1:
          image_paths.remove(image)
          print("can't detect face, remove ", image)
          continue
        det = np.squeeze(bounding_boxes[0,0:4])
        bb = np.zeros(4, dtype=np.int32)
        bb[0] = np.maximum(det[0]-margin/2, 0)
        bb[1] = np.maximum(det[1]-margin/2, 0)
        bb[2] = np.minimum(det[2]+margin/2, img_size[1])
        bb[3] = np.minimum(det[3]+margin/2, img_size[0])
        cropped = img[bb[1]:bb[3],bb[0]:bb[2],:]
        aligned = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
        prewhitened = facenet.prewhiten(aligned)
        img_list.append(prewhitened)
    images = np.stack(img_list)
    return images

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    
    parser.add_argument('model', type=str, 
        help='Could be either a directory containing the meta_file and ckpt_file or a model protobuf (.pb) file')
    parser.add_argument('image_files', type=str, nargs='+', help='Images to compare')
    parser.add_argument('--image_size', type=int,
        help='Image size (height, width) in pixels.', default=160)
    parser.add_argument('--margin', type=int,
        help='Margin for the crop around the bounding box (height, width) in pixels.', default=44)
    parser.add_argument('--gpu_memory_fraction', type=float,
        help='Upper bound on the amount of GPU memory that will be used by the process.', default=1.0)
    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
