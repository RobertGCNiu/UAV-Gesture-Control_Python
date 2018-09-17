# UAV-Gesture-Control
This project is made by Chinese Univeristy of Hong Kong, Shenzhen(CUHKSZ) and Stanford.

The goal is to control the UAV Tello by hand gesture or body pose.

## Simple Control 
You can use the files in Simple-Control. The message is sent as string to Tello and the response will feed back to PC.

## Tellopy Control
The Tellopy can be installed by pip. But When I intall 'av' by pip, the error occured and I can't fix it. The easy method to solve is to use Anaconda by running

```
$conda install av -c conda-forge
```
## Openpose 
Please follow the [Installation Manual](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation.md) to install [Openpose](https://github.com/CMU-Perceptual-Computing-Lab/openpose). Ubuntu version is recommended. All of codes are only checked in Ubuntu 16.04 system. Please make sure all of the required packages have been installed. It will cost almost 30 minutes.

If you have error like <font color=red>'CMake Error at /usr/share/cmake-3.5/Modules/ExternalProject.cmake:1915 (message)'</font> when running Cmake GUI, please run the following code


```
$cd 3rdparty
$git clone https://github.com/CMU-Perceptual-Computing-Lab/caffe.git
```

Now, run CMake GUI to Configure and Generate.

Check OpenPose was properly installed by running it on the default images, video, or webcam: [Quick Start](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/quick_start.md#quick-start).

## Pose Detection by the Camera of Tello
The python codes are updated and can be run directly if you connect your Tello with PC. Please copy the files '/python_tutorial' to your computer path 'openpose/build/examples/python_tutorial'

The following video is the result of [video_effect.py](https://github.com/RobertGCNiu/Tello-Gesture-Control/blob/master/tutorial_python/video_effect.py).
  

<div align=center><img width="600" height="400" src="https://github.com/RobertGCNiu/Tello-Gesture-Control/blob/master/example-video/detection.png"></div>

<div align=center><img width="600" height="400" src="https://github.com/RobertGCNiu/Tello-Gesture-Control/blob/master/example-video/posedetection.gif"></div>

<div align=center><img width="600" height="400" src="https://github.com/RobertGCNiu/Tello-Gesture-Control/blob/master/example-video/Pose_Control.gif"></div>

<div align=center><img width="600" height="400" src= "https://github.com/RobertGCNiu/UAV-Gesture-Control_Python/blob/master/example-video/left.gif"></div>

##Use kNN to classify the pose
The training data sets are collected by 'mat' file. All codes and data sets are [here](https://github.com/RobertGCNiu/UAV-Gesture-Control_Python/tree/master/tutorial_python/kNN)
<div align=center><img width="600" height="400" src= "https://github.com/RobertGCNiu/UAV-Gesture-Control_Python/blob/master/tutorial_python/kNN/trainning_data_sets.png"></div>


