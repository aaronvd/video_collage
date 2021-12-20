import cv2
from datetime import datetime
import shutil
import numpy as np
import os

class collage:
    '''Container object for video recording, interpolation and tiling methods.'''
    
    def __init__(self, 
            fps = 30, 
            length_seconds = 10,
            color_type = None,
            color_rate = 1):
        self.fps = fps
        self.frame_length = int(1/fps * 1000) # in milliseconds
        self.length_seconds = length_seconds
        self.color_type = color_type
        self.color_rate = color_rate
        self.n_frames = length_seconds * fps
        if not os.path.isdir('../Original Videos'):
            os.mkdir('../Original Videos')
        if not os.path.isdir('../Original Videos - Backup'):
            os.mkdir('../Original Videos - Backup')
        if not os.path.isdir('../Resized Videos'):
            os.mkdir('../Resized Videos')
        
    def record(self):
        
        # Create a VideoCapture object
        #cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)   # external webcam
        cap = cv2.VideoCapture(0)                 # computer webcam
        
        # Check if camera opened successfully
        if (cap.isOpened() == False):
            print("Unable to read camera feed")
            
        self.frame_width = int(cap.get(3))
        self.frame_height = int(cap.get(4))
        
        time_label = datetime.now().strftime('%H%M%S')
        out = cv2.VideoWriter(
            '../Original Videos/video'+time_label+'.avi',
            cv2.VideoWriter_fourcc('M','J','P','G'),
            self.fps,
            (self.frame_width, self.frame_height))
        
        for i in range(self.n_frames):
            ret, frame = cap.read()
        
            if ret == True: 
        
                # Write the frame into the output file
                out.write(frame)
        
            # Break the loop
            else:
                break  
        
        # When everything is done, release the video capture and video write objects
        cap.release()
        out.release()
        
        # Closes all the frames
        cv2.destroyAllWindows()
        
        # Backup video file
        shutil.copy('../Original Videos/video'+time_label+'.avi', '../Original Videos - Backup/video'+time_label+'.avi')

    def import_video(self, directory, filename):
        cap = cv2.VideoCapture(directory + filename)
        frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))
        fc = 0
        ret = True
        while (fc < frameCount and ret):
            ret, buf[fc] = cap.read()
            fc += 1
            
        return buf

    def resize_video(self, directory, filename, newHeight, newWidth):
        
        buf0 = self.import_video(directory, filename)
        buf_resized = np.zeros((buf0.shape[0], newHeight, newWidth, buf0.shape[3]), 
                               dtype=np.uint8)
        for i in range(buf0.shape[0]):
            buf_resized[i,:,:,:] = cv2.resize(buf0[i,:,:,:], (newWidth, newHeight)).astype(np.uint8)
            
        return buf_resized
    
    def export_video(self, buf_array, directory, filename):
        frameWidth = buf_array.shape[2]
        frameHeight = buf_array.shape[1]
        
        out = cv2.VideoWriter(directory + filename,
                              cv2.VideoWriter_fourcc('M','J','P','G'),
                              self.fps,
                              (frameWidth, frameHeight))
        for i in range(buf_array.shape[0]):
            out.write(buf_array[i,:,:,:])
            
    def build_collage(self):
        original_filepath = '../Original Videos/'
        resized_filepath = '../Resized Videos/'
        
        original_vid_list = os.listdir(original_filepath)
        resized_vid_list = os.listdir(resized_filepath)
        N_videos = len(original_vid_list)
        side_length = int(np.ceil(np.sqrt(N_videos)))
        
        frame_width = 1920
        frame_height = 1080
        tile_width = int(np.floor(frame_width/side_length))
        tile_height = int(np.floor(frame_height/side_length))
        
        if len(resized_vid_list) < N_videos:
            # If there are no new videos to resize, do nothing
            
            if len(resized_vid_list) == 0:
                # Resize first video
                
                new_filename = original_vid_list[0].split('.')[0] + '_resized.avi'
                resized_video = self.resize_video(original_filepath, original_vid_list[0],
                                             tile_height, tile_width)
                self.export_video(resized_video, resized_filepath, new_filename)
                
                resized_vid_list = os.listdir(resized_filepath)
            
            # Check if dimensions of resized videos are equal to dimensions of our current grid tiles
            if int(cv2.VideoCapture(resized_filepath + resized_vid_list[0]).get(3)) == tile_width:
                # Only resize videos that haven't been resized yet
                
                resized_origin_list = []
                for i in range(len(resized_vid_list)):
                    resized_origin_list.append(resized_vid_list[i].split('_')[0])
                
                for i in original_vid_list:
                    if i.split('.')[0] not in resized_origin_list:
                        new_filename = i.split('.')[0] + '_resized.avi'
                        resized_video = self.resize_video(original_filepath, i,
                                                     tile_height, tile_width)
                        self.export_video(resized_video, resized_filepath, new_filename)
                
            else:
                # Resize all videos to new tile dimensions
                for file in resized_vid_list:
                    os.remove(resized_filepath + file)
                for i in original_vid_list:
                    new_filename = i.split('.')[0] + '_resized.avi'
                    resized_video = self.resize_video(original_filepath, i,
                                                 tile_height, tile_width)
                    self.export_video(resized_video, resized_filepath, new_filename)
                
        #---- Add videos to collage ----#
        resized_vid_list = os.listdir(resized_filepath)
        
        n_start = 10
        collage = np.empty((self.n_frames - n_start, frame_height, frame_width, 3), np.dtype('uint8'))
        
        # Generate random array of positions in grid
        indx_list = np.random.permutation(side_length*side_length)
        indx_height_array, indx_width_array = np.unravel_index(indx_list, (side_length, side_length))
        
        # Place videos
        for i in range(len(resized_vid_list)):
            buf = self.import_video(resized_filepath, resized_vid_list[i])
            if self.color_type == 'tile':
                dist = np.zeros((3), dtype=np.uint8)
                dist[np.random.randint(0,3)] = np.random.randint(50, 100)
                buf += dist[None,None,None,:]

            indx_height = np.arange(indx_height_array[i]*tile_height, (indx_height_array[i]+1)*tile_height)
            indx_width = np.arange(indx_width_array[i]*tile_width, (indx_width_array[i]+1)*tile_width)
            collage[:,indx_height[:,None],indx_width, :] = buf[n_start:,:,:,:]               # omitting early frames to avoid fade in
            
        #plt.imshow(collage[100,:,:,:])
        
        #---- Modify colors ----#
        # color values range from 0-255
        if self.color_type == 'cycle':
            color_val_start = np.random.random_integers(0, 255, (1, 1, 3))
            color_direction = np.array([1, -1])[np.random.random_integers(0, 1, (1, 1, 3))]
            for i in range(collage.shape[0]):
                collage[i,:,:,:] = np.mod(collage[i,:,:,:] + color_val_start + color_direction * int(np.floor(self.color_rate*i)), 255)
        
        # Export collage
        self.export_video(collage, '../', 'collage_temp.avi')












