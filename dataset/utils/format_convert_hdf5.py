import h5py, os
import caffe
import numpy as np
import sys


def pre_process(args):
    idx = args.index('-rsize')
    SIZE_R = int(args[idx+1])
    
    idx = args.index('-csize')
    SIZE_C = int(args[idx+1])

    idx = args.index('-lsize')
    label_size = int(args[idx+1])


    idx = args.index('-train')
    train_text = args[idx+1]


    idx = args.index('-datapl')
    data_path_l = args[idx+1]

    idx = args.index('-datapr')
    data_path_r = args[idx+1]
    
    idx = args.index('-dest')
    h5_path = args[idx+1]

    idx = args.index('-datal')
    data_list = args[idx+1]

    return (SIZE_R, SIZE_C, label_size, train_text, data_path_l, data_path_r, h5_path, data_list)



if __name__ == '__main__':
    
    SIZE_R, SIZE_C, label_size, train_text, data_path_l, data_path_r, h5_path, data_list =pre_process(sys.argv)

    with open(train_text,'r') as T: # traint_text : eg. siam_train.txt
        lines = T.readlines()
    with open('bin_labels.txt','r') as Lab:
        lab_lines = Lab.readlines()
 
    # Create multiple batches
    count = 0
    len_count = 0
    while len_count < len(lines):
            
        X = np.zeros((1000,6,SIZE_C,SIZE_R),dtype='f4') # SIZE_R,SIZE_C
        y = np.zeros((1000,label_size),dtype='f4') # label_size
        for i,l in enumerate(lines[len_count:len_count+1000]):
            # Read the right image's true index
            r_true_idx = int(lines[len_count+i].split(' ')[1])

            sp = l.split(' ')
            labels = lab_lines[len_count+i]
            label = labels.split(' ')
            imgl = caffe.io.load_image(data_path_l+str(len_count+i)+'.png') # data_path : eg. 'processed_data/train/'
            imgl = caffe.io.resize(imgl,(3,SIZE_C,SIZE_R))
            imgr = caffe.io.load_image(data_path_r+str(len_count+i)+'.png') # data_path : eg. 'processed_data/train/'
            imgr = caffe.io.resize(imgr,(3,SIZE_C,SIZE_R))
            img = np.vstack((imgl,imgr))
            X[i] = img
            S = [int(item) for item in (np.asarray(lab_lines[len_count+i].strip('\n').split(' '),dtype='int')-np.asarray(lab_lines[r_true_idx].strip('\n').split(' '),dtype='int'))]
            y[i,:] =  S
        h5_name = h5_path+str(count)+'.h5' # h5 path : eg. 'processed_data/HDF5/train_'
        with h5py.File(h5_name,'w') as H:
            H.create_dataset('X',data=X)
            H.create_dataset('y',data=y)
        with open(data_list,'a') as L: # data_list : eg. 'train_h5_list.txt'
            L.write(os.path.realpath(h5_name)+'\n')   
        
        len_count = len_count + 1000
        count = count + 1

    # Process remaining frames
    if len_count > len(lines):
        len_count = len_count - 1000
        X = np.zeros((len(lines)-len_count,6,SIZE_C,SIZE_R),dtype='f4')
        y = np.zeros((len(lines)-len_count,label_size),dtype='f4')
        for i,l in enumerate(lines[len_count:len(lines)]):
            # Read the right image's true index
            r_true_idx = int(lines[len_count+i].split(' ')[1])
            sp = l.split(' ')
            labels = lab_lines[len_count+i]
            label = labels.split(' ')
            imgl = caffe.io.load_image(data_path_l+str(len_count+i)+'.png') # data_path : eg. 'processed_data/train/'
            imgl = caffe.io.resize(imgl,(3,SIZE_C,SIZE_R))
            imgr = caffe.io.load_image(data_path_r+str(len_count+i)+'.png') # data_path : eg. 'processed_data/train/'
            imgr = caffe.io.resize(imgr,(3,SIZE_C,SIZE_R))
            img = np.vstack((imgl,imgr)) 
            X[i] = img
            S = [int(item) for item in (np.asarray(lab_lines[len_count+i].strip('\n').split(' '),dtype='int')-np.asarray(lab_lines[r_true_idx].strip('\n').split(' '),dtype='int'))]
            y[i,:] =  S
        h5_name = h5_path+str(count)+'.h5'
        with h5py.File(h5_name,'w') as H:
            H.create_dataset('X',data=X)
            H.create_dataset('y',data=y)
        with open(data_list,'a') as L:
            L.write(os.path.realpath(h5_name)+'\n')   

