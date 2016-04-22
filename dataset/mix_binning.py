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
            trans_Y.append(num1-num2)
            num1 = float(linesT[count].split(' ')[2])
            num2 = float(linesT[int(line[1])].split(' ')[2])
            trans_Z.append(num1-num2)
            num1 = float(linesT[count].split(' ')[3])
            num2 = float(linesT[int(line[1])].split(' ')[3])
            rot_X.append(num1-num2)
            num1 = float(linesT[count].split(' ')[5].strip('\n'))
            num2 = float(linesT[int(line[1])].split(' ')[5].strip('\n'))
            rot_Z.append(num1-num2)        
            num1 = float(linesT[count].split(' ')[4])
            num2 = float(linesT[int(line[1])].split(' ')[4])
            rot_Y.append(num1-num2)
            count = count + 1



    return trans_X,trans_Y,trans_Z,rot_X,rot_Y,rot_Z        

def create_labels(dattX,dattY,dattZ,datrX,datrY,datrZ,X,Y,Z,Xr,Yr,Zr,dest):
    with open(dest,'w') as P:
        for item in range(len(dattX)):        
            # Read file
            #idxt = np.where(X>dattX[item])
            #idzt = np.where(Z>dattZ[item])
            #idyt = np.where(Y>dattY[item])
            #idxr = np.where(Xr>datrX[item])
            #idzr = np.where(Zr>datrZ[item])
            #idyr = np.where(Yr>datrY[item])
            #if len(idxt[0]) == 0:
            #    idxt = [[19]]
            #if len(idyt[0]) == 0:
            #    idyt = [[19]]
            #if len(idzt[0]) == 0:
            #    idzt = [[19]]
            #if len(idxr[0]) == 0:
            #    idxr = [[19]]
            #if len(idyr[0]) == 0:
            #    idyr = [[19]]
            #if len(idzr[0]) == 0:
            #    idzr = [[19]]
            #P.write(str(idxt[0][0]-1)+' '+str(idyt[0][0]-1)+' '+str(idzt[0][0]-1)+' '+str(idxr[0][0]-1)+' '+str(idyr[0][0]-1)+' '+str(idzr[0][0]-1)+'\n')
            P.write(str(dattX[item]/max(dattX))+' '+str(dattY[item]/max(dattY))+' '+str(dattZ[item]/max(dattZ))+' '+str(datrX[item]/max(datrX))+' '+str(datrY[item]/max(datrY))+' '+str(datrZ[item]/max(datrZ))+'\n')


if __name__=='__main__':
    orig_bin_path = '/z/Projects/EECS542/EECS542Project/dataset/bin_labels.txt'
    dest_path = '/z/Projects/EECS542/EECS542Project/dataset/bin_labels_new.txt'
    mix_path = '/z/Projects/EECS542/EECS542Project/dataset/siam_train_left.txt'


    X,Y,Z,rotX,rotY,rotZ = minmax(orig_bin_path,mix_path) 

    print "Min and Max translation in X direction: ",min(X),max(X)
    print "Min and Max translation in Z direction: ",min(Z),max(Z)
    print "Min and Max rotation around Y direction: ",min(rotY),max(rotY)

    # Create bins
    Xtlabels = np.linspace(min(X),max(X),20)
    Ytlabels = np.linspace(min(Y),max(Y),20)
    Ztlabels = np.linspace(min(Z),max(Z),20)
    Xrlabels = np.linspace(min(rotX),max(rotX),20)
    Yrlabels = np.linspace(min(rotY),max(rotY),20)
    Zrlabels = np.linspace(min(rotZ),max(rotZ),20)

    # Create label text
    create_labels(X,Y,Z,rotX,rotY,rotZ,Xtlabels,Ytlabels,Ztlabels,Xrlabels,Yrlabels,Zrlabels,dest_path)
