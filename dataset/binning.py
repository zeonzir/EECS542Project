import sys
import os
import glob
import numpy as np

def minmax(files,path):
    trans_X = []
    trans_Y = []
    trans_Z = []
    rot_X = []
    rot_Y = []
    rot_Z = []

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
                    trans_Y.append(Rt[1,-1])
                    trans_Z.append(Rt[-1,-1])
                    # Rt matrix to Euler conversion
                    if Rt[-1,0] != -1 or Rt[-1,0] != 1:
                        theta = -np.arcsin(Rt[-1,0])
                        psi = np.arctan2(Rt[-1,1]/np.cos(theta),Rt[-1,-1]/np.cos(theta))
                        phi = np.arctan2(Rt[1,0]/np.cos(theta),Rt[1,0]/np.cos(theta))
                    else:
                        phi = 0
                        if Rt[-1,0]==-1:
                            theta = 90.0
                            psi = phi + np.arctan2(Rt[0,1],Rt[0,2])
                        else:
                            theta = -90.0
                            psi = -phi + np.arctan2(-Rt[0,1],-Rt[0,2])

                    assert(abs(theta)<=np.pi)    
                    assert(abs(psi)<=np.pi)    
                    assert(abs(phi)<=np.pi)    
                    rot_X.append(psi*180/np.pi)
                    rot_Y.append(theta*180/np.pi)
                    rot_Z.append(phi*180/np.pi)        



    return trans_X,trans_Y,trans_Z,rot_X,rot_Y,rot_Z        

def create_labels(files,dattX,dattY,dattZ,datrX,datrY,datrZ,X,Z,Y,dest):
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
    pose_path = '/media/zeonzir/Data/EECS542/Project/EECS542Project/dataset/poses/'
    dest_path = '/media/zeonzir/Data/EECS542/Project/EECS542Project/dataset/bin_labels_old.txt'


    files = os.listdir(pose_path)
    X,Y,Z,rotX,rotY,rotZ = minmax(files,pose_path) 

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
    create_labels(files,X,Y,Z,rotX,rotY,rotZ,Xlabels,Zlabels,Ylabels,dest_path)
