### Project Description:

This Project is part of CSE 546 - Cloud Computing course

The architecture of the application is as follows - 

![Alt text](https://github.com/PradnyaC11/Video-Analysis-Service/blob/main/architecture.png "Architecture Diagram")

This is a video analysis application that uses two Lambda functions to implement a multi-stage pipeline to process videos sent by users.
1. The pipeline starts with a user uploading a video to the input bucket.
2. Stage 1: The video-splitting function splits the video into frames and chunks them into the group-of-pictures (GoP) using FFmpeg. It stores this group of pictures in an intermediate stage-1 bucket.
3. Stage 2: The face-recognition function extracts the faces in the pictures using a Single Shot MultiBox Detector (SSD) algorithm and uses only the frames that have faces in them for face recognition. It uses a pre-trained CNN model (ResNet-34) for face
recognition and outputs the name of the extracted face. The final output is stored in the output bucket.

We have used AWS Lambda to implement the functions and AWS S3 to store the data required for the functions. 

