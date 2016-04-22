import sys
import os
import glob
import numpy as np

def minmax(path,mix_path):
    # Upgrade: Open new file from training and perform subtraction
    trans_X = []
    trans_Y = []
    trans_Z = []
    rot_X = []
    rot_Y = []
    rot_Z = []
    
    fileT = open(path,'r')
    linesT = fileT.readlines()

    with open(mix_path,'r') as fileM:
        # Read the file
        lines = fileM.readlines()
        # Process all the lines find required values
        count = 0
        for line in lines:
            line = line.split(' ')
            # 2nd component spells the diff category
            num1 = float(linesT[count].split(' ')[0])
            num2 = float(linesT[int(line[1])].split(' ')[0])
            trans_X.append(num1 - num2)
            num1 = float(linesT[count].split(' ')[1])
            num2 = float(linesT[int(line[1])].split(' ')[1])
            trans_Z.append(num1-num2)
            num1 = float(linesT[count].split(' ')[2].strip('\n'))
            num2 = float(linesT[int(line[1])].split(' ')[2].strip('\n'))
            rot_Y.append(num1-num2)        
            count = count + 1



    return trans_X,trans_Z,rot_Y        

def create_labels(dattX,dattZ,datrY,X,Z,Y,dest):
    with open(dest,'w') as P:
        for item in range(len(dattX)):        
            # Read file
            idx = np.where(X>dattX[item])
            idz = np.where(Z>dattZ[item])
            idy = np.where(Y>datrY[item])
            if len(idx[0]) == 0:
                idx = [[19]]
            if len(idy[0]) == 0:
                idy = [[19]]
            if len(idz[0]) == 0:
                idz = [[19]]
            P.write(str(idx[0][0]-1)+' '+str(idz[0][0]-1)+' '+str(idy[0][0]-1)+'\n')
            #P.write(str(dattX[item])+' '+str(dattZ[item])+' '+str(datrY[item]/max(datrY))+'\n')


if __name__=='__main__':
    orig_bin_path = '/media/zeonzir/Data/EECS542/Project/EECS542Project/dataset/bin_labels.txt'
    dest_path = '/media/zeonzir/Data/EECS542/Project/EECS542Project/dataset/bin_labels_new.txt'
    mix_path = '/media/zeonzir/Data/EECS542/Project/EECS542Project/dataset/siam_train_left.txt'


    X,Z,rotY = minmax(orig_bin_path,mix_path) 

    print "Min and Max translation in X direction: ",min(X),max(X)
    print "Min and Max translation in Z direction: ",min(Z),max(Z)
    print "Min and Max rotation around Y direction: ",min(rotY),max(rotY)

    # Create bins
    Xlabels = np.linspace(min(X),max(X),20)
    Zlabels = np.linspace(min(Z),max(Z),20)
    Ylabels = np.linspace(min(rotY),max(rotY),20)

    print "X bins: ",Xlabels
    print "Z bins: ",Zlabels
    print "Y bins: ",Ylabels

    # Create label text
    create_labels(X,Z,rotY,Xlabels,Zlabels,Ylabels,dest_path)
