import sys
import os
from shutil import copyfile
import glob

if __name__=='__main__':
    cur_path = os.getcwd()
    file_path = os.path.join(cur_path,'dataset/sequences')

    dirs = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21']
    train_dirs = ['00','01','02','03','04','05','06','07','08','09','10']

    # Create folder train in processed_data
    train_path = os.path.join(cur_path,'processed_data/train_right')
    os.makedirs(train_path)

    # Access GT pose data
    pose_path = os.path.join(cur_path,'poses')

    # Create siam_train.txt
    f = open('siam_train.txt','w')
    
    count = 0
    head = 'KITTI_'
    for index in train_dirs:
        temp_file_path = os.path.join(file_path,index+'/image_3')
        file_pose_path = os.path.join(pose_path,index+'.txt')

        pose_file = open(file_pose_path,'r')
        imgs = os.listdir(temp_file_path)
        for img in imgs:
            if img.endswith(".png"):
                img_from_path = os.path.join(temp_file_path,img)
                img_to_path = os.path.join(train_path,head+str(count)+'.png')

                # Copy file
                copyfile(img_from_path,img_to_path)
                # Append name and label into siam_train.txt
                line = pose_file.readline()
                sp_line = line.split(' ')
                f.write(head+str(count)+'.png '+ ' '.join(sp_line))
                
                count = count + 1

        pose_file.close()

    f.close()
        
