# Applying_filter_in_face

## Description
This repository contains python implmentation of various snapchat like face filters and masks using opencv and dlib.

Dlib used for finding face and detect landmarks which uses a Histogram of Oriented Gradients (HOG) feature combined with a linear classifier, an image pyramid, and sliding window detection scheme to detect faces. Then it finds the 68 facial landmarks using an Ensemble of Regression Trees to detect the face characteristics and to estimate the tilt angle of the face.

## Currently following filters are available:
- face_mask Filter
- glass Filter
- Moustache Filter
- Hat Filter
- mustache Filter
- thug life Filter

## Dependencies
- Python
- The program makes use of Dlib-facial feature points
- OpenCV
- Tkinter
- Shape predictor 68 face landmark points Model

## How to use?
- Git clone repository:
    
      git clone https://github.com/kunalgupta777/OpenCV-Face-Filters

- Make sure to install the dependencies:

      pip install dlib
      pip install opencv-python
      conda install tk

- Executing program
  Before running the program, please navigate dlib model to the model folder. \
  To run type 
      
      python gui.py in terminal
      
- changes filters \
  click on bifferent filter buttons 
  
## outputs
![1](https://github.com/rjnp2/Applying_filter_in_face/blob/main/icon/gif.gif) \
fig: System working operates

![1](https://github.com/rjnp2/Applying_filter_in_face/blob/main/icon/filter_.png) \
fig: filters which can be apply

![1](https://github.com/rjnp2/Applying_filter_in_face/blob/main/filter_video.gif)

# Thank You






