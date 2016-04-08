import sys
import os
import glob
import numpy as np

def minmax(files,path):
    trans_X = []
    trans_Z = []
    rot_Y = []
    for fileT in files:
        # Read the file
        if fileT.endswith(".txt"):
            with open(path+fileT,'r') as P:
                lines = P.readlines()
                
                # Process all the lines find required values
                for line in lines:
                    line = line.split(' ')
                    Rt = np.asarray([[float(line[0]), float(line[1]), float(line[2]), float(line[3])],
                                    [float(line[4]), float(line[5]), float(line[6]), float(line[7])],
                                    [float(line[8]), float(line[9]), float(line[10]), float(line[11])]])
                    trans_X.append(Rt[0,-1])
                    trans_Z.append(Rt[-1,-1])
                    v = np.asarray([1,0,0,1])
                    vR = Rt.dot(v)
                    beta = np.arccos(v[0:3].dot(vR)/np.linalg.norm(vR)/np.linalg.norm(v[0:3]))*180/np.pi
                    rot_Y.append(beta)

    return trans_X,trans_Z,rot_Y        

def create_labels(files,datX,datZ,datY,X,Z,Y,dest):
    with open(dest,'w') as P:
        for item in range(len(datX)):        
            # Read file
            idx = np.where(X>datX[item])
            idz = np.where(Z>datZ[item])
            idy = np.where(Y>datY[item])
            if len(idx[0]) == 0:
                idx = [[19]]
            if len(idy[0]) == 0:
                idy = [[19]]
            if len(idz[0]) == 0:
                idz = [[19]]
            P.write(str(idx[0][0]-1)+' '+str(idz[0][0]-1)+' '+str(idy[0][0]-1)+'\n')


if __name__=='__main__':
    pose_path = '/media/zeonzir/Data/EECS542/Project/EECS542Project/dataset/poses/'
    dest_path = '/media/zeonzir/Data/EECS542/Project/EECS542Project/dataset/bin_labels.txt'


    files = os.listdir(pose_path)
    X,Z,rotY = minmax(files,pose_path) 

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
    create_labels(files,X,Z,rotY,Xlabels,Zlabels,Ylabels,dest_path)
