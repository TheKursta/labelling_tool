#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 22:55:53 2020

@author: icv
"""

import os
import cv2
import numpy as np
import math
#import pandas as pd
#pip install keyboard
#import keyboard

root_dir = "/home/icv/Desktop/test_fold/"
frame_count = 0
def read_all_video_frames (vid_path):
    frameslist = []
    frame_count = 0
    print(vid_path)
    # load video capture from file
    cap = cv2.VideoCapture(str(vid_path))
    
    while not cap.isOpened():
        cap = cv2.VideoCapture(vid_path)
        cv2.waitKey(1000)
        print ("Wait for the header")
    boolen = 1
    while boolen:
        boolen, np_frame = cap.read() # get the frame
        try:
            np_frame = cv2.cvtColor(np_frame, cv2.COLOR_BGR2GRAY)
        except:
            np_frame = np.zeros([960,540,1],dtype=np.uint8)

        # The frame is ready and already captured
        # cv2.imshow('video', frame)

        # store the current frame in as a numpy array
        #np_frame = cv2.imread('video', frame)
        frameslist.append(np_frame)
        """
    
        if cv2.waitKey(10) == 27:
            #if we want to exit early
            break
        if cap.get(1) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            # If the number of captured frames is equal to the total number of frames,
            # we stop
            print("frame nrs match")
            break
        """
        
        if frame_count == int(math.floor(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
            break
        
    all_frames = frameslist
    cap.release()
    return all_frames
    

subject = input("please enter subject id: ")
frame_nr = 0
framestamp1 = 0
framestamp2 = 0
 
for filename in os.listdir(root_dir):
    if filename.startswith(str(subject)):
        #reading video
        win_name = str(os.path.join(root_dir, filename))
        vid_frames = read_all_video_frames(win_name)
        print(len(vid_frames))
        
        #TODO ADD ON-DISPLAY INSTRUCTIONS
        while True:
            #showing the display
            frame = vid_frames[frame_nr]
            frame = cv2.resize(frame,(960,540))
            cv2.namedWindow(filename, cv2.WINDOW_NORMAL)
            cv2.imshow(filename, frame)
            
            #waiting till the key press
            key = cv2.waitKey(5000)

            #nav right/left/framestamp/restart
            if key == ord('d'):
                print(frame_nr)
                frame_nr += 1
                continue
                
            if key == ord('a'):
                frame_nr -= 1
                continue
                
            if key == ord('s'):
                framestamp = frame_nr
                continue
            if key == ord('w'):
                frame_nr = 0
                framestamp1 = 0
                framestamp2 = 0
                continue
            if key == ord('q'):
                break
            cv2.destroyAllWindows()
            """    
            if key == ord('q') or frame_nr == len(vid_frames-1):
                with open(win_name[:-4]+".txt","w+") as label_file:
                    label_file.write(framestamp1+"\t"+framestamp2+"\n")
                label_file.close()
                break
            """        
                
                    
                    
                
                
                
        
                
            
            
            
            
        
            
            
            
            
            
        
    