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
#importing threading with only one process
from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes = 1)

window = tk.Tk()
window.withdraw()
window.lift()

#input dialog box for root folder of videos
#root_dir = simpledialog.askstring(title = " ", prompt = "Please enter the root directory of videos")
#root_dir = "C:\\Users\\klavs\\Desktop\\1344"

#path to root folder of all vids
root_dir = "/home/icv/Desktop/1348_labelling"
frame_count = 0

files_iter = []
first_exec = True

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
framestamp3 = 0
abnormal_limbs = 0
heavy_occlusion = 0
low_occlusion = 0
non_correlating = 0
other = 0
video_emotion = ""



for filename in os.listdir(root_dir):
     if filename.startswith(str(subject)) and filename.endswith(".mp4"):
         total_vid_nr += 1
     if filename.startswith(str(subject)) and filename.endswith(".mp4") and os.path.exists(os.path.join(root_dir,filename[:-4]+".txt")):
         completed_vid_nr += 1

#creates a list of video filenames that havent been labelled yet        
for filename in os.listdir(root_dir):
    if (filename.startswith(str(subject)) and filename.endswith(".mp4")) and not os.path.exists(os.path.join(root_dir,filename[:-4]+".txt")):
        files_iter.append(filename) 
        
#starts working through videos that havent been labelled yet
for i in range(0,len(files_iter)):
    if first_exec == True:
        full_path = str(os.path.join(root_dir, files_iter[i]))
        vid_frames = read_all_video_frames(full_path)        
        print(len(vid_frames))
        
        if len(files_iter)>=2:        
            full_path = str(os.path.join(root_dir, files_iter[i+1]))
            print(full_path)
            future_vid = pool.apply_async(read_all_video_frames, args = (full_path,))
        
    if first_exec == False:
        vid_frames = future_vid.get()
        print("The file now that is being labelled is", files_iter[i])
        if i!=(len(files_iter)-1):            
            full_path = str(os.path.join(root_dir, files_iter[i+1]))
            future_vid = pool.apply_async(read_all_video_frames, args = (full_path,))        
        
    #setting video logic variables
    filename = files_iter[i]
    framestamp_nr = 1
    frame_nr = 0
    framestamp1 = 0
    framestamp2 = 0
    framestamp3 = 0
    abnormal_limbs = 0
    heavy_occlusion = 0
    low_occlusion = 0
    non_correlating = 0
    other = 0
    cv2.destroyAllWindows()
    
    #emotions based on the filename
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

    if "7" in filename[-6:-7]:
        video_emotion = "Happiness"
           
    while True:
        first_exec = False
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
        cv2.putText(frame,"Reset marks w", (900,180), 1, 1, (255,0,0), 1, cv2.LINE_AA)
        cv2.putText(frame,"Non correlating g", (800,210), 1, 1, (255,0,0), 1, cv2.LINE_AA)
        cv2.putText(frame,"Abnormal limb behaviour t", (800,240), 1, 1, (255,0,0), 1, cv2.LINE_AA)
        cv2.putText(frame,"Low-occlusion u", (800,270), 1, 1, (255,0,0), 1, cv2.LINE_AA)
        cv2.putText(frame,"Heavy-occlusion p", (800,300), 1, 1, (255,0,0), 1, cv2.LINE_AA)
        cv2.putText(frame,"Other x", (900,330), 1, 1, (255,0,0), 1, cv2.LINE_AA)        
        #variables
        cv2.putText(frame,"Frame_nr: "+str(frame_nr), (10,50), 0, 1, (0,0,255), 2, cv2.LINE_AA)
        cv2.putText(frame,"Emotion: "+str(video_emotion), (10,100), 0, 1, (0,0,255), 2, cv2.LINE_AA)
        cv2.putText(frame,"Framepoints listed: "+str(framestamp_nr-1)+" Frame: "+str(framestamp1)+" and "+str(framestamp2)+" and "+str(framestamp3)+" Videos completed "+str(completed_vid_nr)+"/"+str(total_vid_nr), (150,680), 1, 1, (0,255,0), 1, cv2.LINE_AA)
        cv2.putText(frame,"Non-corellating mark "+str(non_correlating)+" Abnormal limbs mark "+str(abnormal_limbs)+" Low-occlusion mark "+str(low_occlusion)+" Heavy-occlusion mark "+str(heavy_occlusion)+" Other mark "+str(other), (150,700), 1, 1, (0,255,0), 1, cv2.LINE_AA)
        cv2.imshow(filename, frame)
        
        #waiting till the key press
        key = cv2.waitKey(5000000)

        #nav right/left/framestamp/restart
        if key == ord('d'):
            print(frame_nr)
            if frame_nr < len(vid_frames)-6:
                frame_nr += 3
                continue
            #save all marks if end of video is reached and all marks are present
            else:
                if framestamp_nr  == 4:
                    completed_vid_nr += 1
                    if framestamp2>=framestamp1:                    
                        with open (full_path[:-4]+'.txt','w+') as label_file:
                            label_file.write(str(framestamp1)+"\t"+str(framestamp2)+"\t"+str(framestamp3)+"\t"+str(non_correlating)+"\t"+str(abnormal_limbs)+"\t"+str(low_occlusion)+"\t"+str(heavy_occlusion)+"\t"+str(other)+"\n")
                            #label_file.write("{}\t{}".format(framestamp1, framestamp2))
                            label_file.close()
                        
                    if framestamp1>framestamp2:                    
                        with open (full_path[:-4]+'.txt','w+') as label_file:
                            label_file.write(str(framestamp2)+"\t"+str(framestamp1)+"\t"+str(framestamp3)+"\t"+str(non_correlating)+"\t"+str(abnormal_limbs)+"\t"+str(low_occlusion)+"\t"+str(heavy_occlusion)+"\t"+str(other)+"\n")
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
            
            if framestamp_nr == 3:
                framestamp3 = framestamp
                framestamp_nr += 1
                print("Framestamp recorded")  
                time.sleep(0.1)  
                
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
            framestamp3 = 0
            abnormal_limbs = 0
            heavy_occlusion = 0
            low_occlusion = 0
            non_correlating = 0
            other = 0
            continue
        
        if key == ord('q'):
            print("Goodbye friend!")
            cv2.destroyAllWindows()
            break
        #mark key bindings
        if key == ord('g'):
            print("Non-correlating emotion!")
            non_correlating = 1
            continue

        if key == ord('t'):
            print("Abnormal limbs!")
            abnormal_limbs = 1
            continue
        
        if key == ord('u'):
            print("Low-occlusion!")
            low_occlusion = 1
            continue
        
        if key == ord('p'):
            print("Heavy-occlusion!")
            heavy_occlusion = 1
            continue

        if key == ord('x'):
            print("Other!")
            other = 1
            continue
        
        if key == ord('e'):
            if framestamp_nr!=4:
                print("Please choose three frame points. Start/End/Middle")
                continue
            
            else:
                completed_vid_nr += 1                       
                if framestamp2>=framestamp1:                    
                    with open (full_path[:-4]+'.txt','w+') as label_file:
                        label_file.write(str(framestamp1)+"\t"+str(framestamp2)+"\t"+str(framestamp3)+"\t"+str(non_correlating)+"\t"+str(abnormal_limbs)+"\t"+str(low_occlusion)+"\t"+str(heavy_occlusion)+"\t"+str(other)+"\n")
                        #label_file.write("{}\t{}".format(framestamp1, framestamp2))
                        label_file.close()
                    
                if framestamp1>framestamp2:                    
                    with open (full_path[:-4]+'.txt','w+') as label_file:
                        label_file.write(str(framestamp2)+"\t"+str(framestamp1)+"\t"+str(framestamp3)+"\t"+str(non_correlating)+"\t"+str(abnormal_limbs)+"\t"+str(low_occlusion)+"\t"+str(heavy_occlusion)+"\t"+str(other)+"\n")
                        #label_file.write("{}\t{}".format(framestamp2, framestamp1))     
                        label_file.close()
                
                print("Label file saved succesfully!")
                print("{}\t{}".format(framestamp1, framestamp2))
                cv2.destroyAllWindows()
                break
            
        cv2.destroyAllWindows()
            
            
print("time it took: ", start - time.time())
                    
                    
                
                
                
        
                
            
            
            
            
        
            
            
            
            
            
        
    