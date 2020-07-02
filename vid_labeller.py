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
import time
import tkinter as tk
from tkinter import simpledialog

#root directory 
window = tk.Tk()
window.withdraw()
window.lift()
#input dialog
#root_dir = simpledialog.askstring(title = " ", prompt = "Please enter the root directory of videos")
root_dir = "C:\\Users\\klavs\\Desktop\\1344"

frame_count = 0

start = time.time()

#reading all the videoframes into the list
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
            np_frame = cv2.cvtColor(np_frame, cv2.COLOR_GRAY2BGR)
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
    
window = tk.Tk()
window.withdraw()
window.lift()

#input dialog
subject = simpledialog.askstring(title = " ", prompt = "Which subject to label?")
#subject = input("please enter subject id: ")

#set vars
completed_vid_nr = 0
total_vid_nr = 0
frame_nr = 0
framestamp1 = 0
framestamp2 = 0
video_emotion = ""

for filename in os.listdir(root_dir):
     if filename.startswith(str(subject)) and filename.endswith(".mp4"):
         total_vid_nr += 1
     if filename.startswith(str(subject)) and filename.endswith(".mp4") and os.path.exists(os.path.join(root_dir,filename[:-4]+".txt")):
         completed_vid_nr += 1
         
for filename in os.listdir(root_dir):
    if (filename.startswith(str(subject)) and filename.endswith(".mp4")) and not os.path.exists(os.path.join(root_dir,filename[:-4]+".txt")):
        #resetting vid specific values
        framestamp_nr = 1
        frame_nr = 0
        framestamp1 = 0
        framestamp2 = 0
        cv2.destroyAllWindows()
        #reading video
        full_path = str(os.path.join(root_dir, filename))
        vid_frames = read_all_video_frames(full_path)        
        print(len(vid_frames))
        
        #TODO Add different emotions based on codes
        print(filename[-6:-5])
        if "1" in filename[-6:-5]:
            video_emotion = "Disgust"
            
        if "2" in filename[-6:-5]:
            video_emotion = "Surprise"

        if "3" in filename[-6:-5]:
            video_emotion = "Sadness"

        if "4" in filename[-6:-5]:
            video_emotion = "Anger"

        if "5" in filename[-6:-5]:
            video_emotion = "Fear"

        if "6" in filename[-6:-5]:
            video_emotion = "Neutral"

        if "7" in filename[-6:-]:
            video_emotion = "Happiness"
        
           
        while True:
            #showing the display
            frame = vid_frames[frame_nr]
            frame = cv2.resize(frame,(1024,720))
            cv2.namedWindow(filename, cv2.WINDOW_AUTOSIZE)
            
            #legends
            cv2.putText(frame,"Forward d", (900,30), 1, 1, (255,0,0), 1, cv2.LINE_AA)
            cv2.putText(frame,"Backward a", (900,60), 1, 1, (255,0,0), 1, cv2.LINE_AA)
            cv2.putText(frame,"Framestamp s", (900,90), 1, 1, (255,0,0), 1, cv2.LINE_AA)
            cv2.putText(frame,"Save press e", (900,120), 1, 1, (255,0,0), 1, cv2.LINE_AA)
            cv2.putText(frame,"Quit press q", (900,150), 1, 1, (255,0,0), 1, cv2.LINE_AA)
            cv2.putText(frame,"Reset w", (900,180), 1, 1, (255,0,0), 1, cv2.LINE_AA)
            
            #variables
            cv2.putText(frame,"Frame_nr: "+str(frame_nr), (10,50), 0, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(frame,"Emotion: "+str(video_emotion), (10,100), 0, 1, (0,0,255), 2, cv2.LINE_AA)
            cv2.putText(frame,"Framepoints listed: "+str(framestamp_nr)+" "+"Frame: "+str(framestamp1)+" "+"and "+str(framestamp2)+" "+"Videos completed "+str(completed_vid_nr-1)+"/"+str(total_vid_nr), (300,700), 1, 1, (0,255,0), 1, cv2.LINE_AA)   
            cv2.imshow(filename, frame)
            
            #waiting till the key press
            key = cv2.waitKey(5000000)

            #nav right/left/framestamp/restart
            if key == ord('d'):
                print(frame_nr)
                if frame_nr < len(vid_frames)-6:
                    frame_nr += 3
                    continue
                else:
                    if framestamp_nr  == 3:
                        completed_vid_nr += 1
                        if framestamp2>=framestamp1:                    
                            with open (full_path[:-4]+'.txt','w+') as label_file:
                                label_file.write(str(framestamp1)+"\t"+str(framestamp2)+"\n")
                                #label_file.write("{}\t{}".format(framestamp1, framestamp2))
                                label_file.close()
                            
                        if framestamp1>framestamp2:                    
                            with open (full_path[:-4]+'.txt','w+') as label_file:
                                label_file.write(str(framestamp2)+"\t"+str(framestamp1)+"\n")
                                #label_file.write("{}\t{}".format(framestamp2, framestamp1))     
                                label_file.close()
                        
                        print("Label file saved succesfully!")
                        print("{}\t{}".format(framestamp1, framestamp2))
                        cv2.destroyAllWindows()
                        break
                
            if key == ord('a'):
                if frame_nr>3:    
                    frame_nr -= 3
                continue
                
            if key == ord('s'):
                framestamp = frame_nr
                
                if framestamp_nr == 2:
                    framestamp2 = framestamp
                    framestamp_nr += 1
                    print("Framestamp recorded")
                    time.sleep(0.1)
                    
                if framestamp_nr == 1:
                    framestamp1 = framestamp
                    framestamp_nr += 1
                    print("Framestamp recorded")  
                    time.sleep(0.1)
                continue
            
            if key == ord('w'):
                frame_nr = 0
                framestamp_nr = 1
                framestamp1 = 0
                framestamp2 = 0
                continue
            
            if key == ord('q'):
                print("Goodbye friend!")
                cv2.destroyAllWindows()
                break
            
            if key == ord('e'):
                if framestamp_nr!=3:
                    print("Please choose two frame points")
                    continue
                
                else:
                    completed_vid_nr += 1                       
                    if framestamp2>=framestamp1:                    
                        with open (full_path[:-4]+'.txt','w+') as label_file:
                            label_file.write(str(framestamp1)+"\t"+str(framestamp2)+"\n")
                            #label_file.write("{}\t{}".format(framestamp1, framestamp2))
                            label_file.close()
                        
                    if framestamp1>framestamp2:                    
                        with open (full_path[:-4]+'.txt','w+') as label_file:
                            label_file.write(str(framestamp2)+"\t"+str(framestamp1)+"\n")
                            #label_file.write("{}\t{}".format(framestamp2, framestamp1))     
                            label_file.close()
                    
                    print("Label file saved succesfully!")
                    print("{}\t{}".format(framestamp1, framestamp2))
                    cv2.destroyAllWindows()
                    break
                
            cv2.destroyAllWindows()
            
            
print("time it took: ", start - time.time())
                    
                    
                
                
                
        
                
            
            
            
            
        
            
            
            
            
            
        
    