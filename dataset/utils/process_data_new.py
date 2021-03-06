import sys
import os
from shutil import copyfile
import glob
import numpy as np
import cv2

if __name__=='__main__':
    cur_path = os.getcwd()
    file_path = os.path.join(cur_path,'dataset/sequences')

    dirs = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21']
    train_dirs = ['00','01','02','03','04','05','06','07','08','09','10']
    test_dirs = ['11','12','13','14','15','16','17','18','19','20','21']
    # Create folder train in processed_data
        
    train_path_l = os.path.join(cur_path,'processed_data/test_left') # Change
    train_path_r = os.path.join(cur_path,'processed_data/test_right') # Change
    os.makedirs(train_path_l)
    os.makedirs(train_path_r)

    # Access GT pose data
    pose_path = os.path.join(cur_path,'poses')

    # Create siam_train.txt
    f_l = open('siam_test_left.txt','w') # change
    f_r = open('siam_test_right.txt','w') # change

    MEANIMG_R = np.zeros((227,227,3))
    MEANIMG_L = np.zeros((227,227,3))
    count = 0
    headl = '/media/zeonzir/Data/EECS542/Project/EECS542Project/dataset/processed_data/test_left/KITTI_' # Change
    headr = '/media/zeonzir/Data/EECS542/Project/EECS542Project/dataset/processed_data/test_right/KITTI_' # Change

    for index in test_dirs:
        temp_file_path_l = os.path.join(file_path,index+'/image_2') #change
        temp_file_path_r = os.path.join(file_path,index+'/image_2') #change
    

        imgs = os.listdir(temp_file_path_l)
        imgs_r = os.listdir(temp_file_path_r)

        for img in imgs:
            if img.endswith(".png"):
                # Holding left image constant pick -+7 right image
                img_from_path_l = os.path.join(temp_file_path_l,img)
                img_to_path_l = os.path.join(train_path_l,headl+str(count)+'.png')
                
                # pick a random integer in the space of -+7
                r_idx = np.random.randint(count-7,count+7)
                r_idx = max(r_idx,0)
                r_idx = min(r_idx,len(imgs)-1)

                # Randomly crop a 227x227 section of the image
                IMG_L = cv2.imread(img_from_path_l)
                [r,c,chnl] = IMG_L.shape
                newr = np.random.randint(0,r-227-1)
                newc = np.random.randint(0,c-227-1)
                IMG_L = IMG_L[newr:newr+227,newc:newc+227,:]
                MEANIMG_L = MEANIMG_L + IMG_L

                img_from_path_r = os.path.join(temp_file_path_r,imgs_r[r_idx])
                img_to_path_r = os.path.join(train_path_r,headr+str(count)+'.png')

                IMG_R = cv2.imread(img_from_path_r)
                [r,c,chnl] = IMG_R.shape
                IMG_R = IMG_R[newr:newr+227,newc:newc+227,:]
                MEANIMG_R = MEANIMG_R + IMG_R
                #cv2.namedWindow("Trial",0)
                #cv2.imshow("Trial",IMG)
                #cv2.waitKey(-1)

                # Write file
                cv2.imwrite( img_to_path_l, IMG_L );
                cv2.imwrite( img_to_path_r, IMG_R );
                #copyfile(img_from_path,img_to_path)
                # Append name and label into siam_train.txt
                f_l.write(os.path.realpath(headl+str(count)+'.png')+' '+str(r_idx)+'\n')
                f_r.write(os.path.realpath(headr+str(count)+'.png')+'\n')
                
                count = count + 1

        #pose_file.close()

    f_l.close()
    f_r.close()

    MEANIMG_R = MEANIMG_R / (count+1)
    MEANIMG_L = MEANIMG_L / (count+1)
    # Find mean and subtract from the images
    dest_path_l = '/media/zeonzir/Data/EECS542/Project/EECS542Project/dataset/processed_data/test_left/'
    imgs = os.listdir(dest_path_l)
    for img in imgs:
        if img.endswith(".png"):
            img_path = os.path.join(dest_path_l,img)
            IMG = cv2.imread(img_path)
            IMG = IMG - MEANIMG_L
            IMG = IMG/255.
            cv2.imwrite(img_path,IMG)
        
    dest_path_r = '/media/zeonzir/Data/EECS542/Project/EECS542Project/dataset/processed_data/test_right/'
    imgs = os.listdir(dest_path_r)
    for img in imgs:
        if img.endswith(".png"):
            img_path = os.path.join(dest_path_r,img)
            IMG = cv2.imread(img_path)
            IMG = IMG - MEANIMG_R
            IMG = IMG/255.
            cv2.imwrite(img_path,IMG)
