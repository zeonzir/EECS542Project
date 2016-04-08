import caffe
import lmdb
from PIL import Image
import sys
import numpy as np
import os

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
    lmdb_path = args[idx+1]

    idx = args.index('-datal')
    data_list = args[idx+1]

    return (SIZE_R, SIZE_C, label_size, train_text, data_path_l, data_path_r, lmdb_path, data_list)





if __name__ == '__main__':
    
    SIZE_R, SIZE_C, label_size, train_text, data_path_l, data_path_r, lmdb_path, data_list =pre_process(sys.argv)

    with open(train_text,'r') as T: # traint_text : eg. siam_train.txt
        lines = T.readlines()

    # Create multiple batches
    count = 0
    len_count = 0
    while len_count < len(lines):
        lmdb_cur_path = lmdb_path+str(count) # eg. processed_data/LMDB/image-lmdb<number>
        in_db = lmdb.open(lmdb_cur_path, map_size=int(1e10), create=True)
        with in_db.begin(write=True) as in_txn:
            for i,l in enumerate(lines[len_count:len_count+1000]):
                # load image:
                # - as np.uint8 {0, ..., 255}
                # - in BGR (switch from RGB)
                # - in Channel x Height x Width order (switch from H x W x C)
                im_l = np.array(Image.open(data_path_l+str(len_count+i)+'.png')) # or load whatever ndarray you need
                im_l = im_l[:,:,::-1]
                im_l = im_l.transpose((2,0,1))
                im_r = np.array(Image.open(data_path_r+str(len_count+i)+'.png')) # or load whatever ndarray you need
                im_r = im_r[:,:,::-1]
                im_r = im_r.transpose((2,0,1))
                # Stack left and right images vertically
                im = np.vstack((im_l, im_r))
                im_dat = caffe.io.array_to_datum(im)
                in_txn.put('{:0>10d}'.format(i), im_dat.SerializeToString())
        in_db.close()

        with open(data_list,'a') as L: # data_list : eg. 'train_lmdb_list.txt'
            L.write(os.path.realpath(lmdb_cur_path)+'\n')

        len_count = len_count + 1000
        count = count + 1

    # Process remaining frames
    if len_count > len(lines):
        len_count = len_count - 1000
        lmdb_cur_path = lmdb_path+str(count) # eg. processed_data/LMDB/image-lmdb<number>
        in_db = lmdb.open(lmdb_cur_path, map_size=int(1e12),create=True)
        with in_db.begin(write=True) as in_txn:
            for i,l in enumerate(lines[len_count:len_count+1000]):
                # load image:
                # - as np.uint8 {0, ..., 255}
                # - in BGR (switch from RGB)
                # - in Channel x Height x Width order (switch from H x W x C)
                im_l = np.array(Image.open(data_path_l+str(len_count+i)+'.png')) # or load whatever ndarray you need
                im_l = im_l[:,:,::-1]
                im_l = im_l.transpose((2,0,1))
                im_r = np.array(Image.open(data_path_r+str(len_count+i)+'.png')) # or load whatever ndarray you need
                im_r = im_r[:,:,::-1]
                im_r = im_r.transpose((2,0,1))
                # Stack left and right images vertically
                im = np.vstack((im_l, im_r))
                im_dat = caffe.io.array_to_datum(im)
                in_txn.put('{:0>10d}'.format(i), im_dat.SerializeToString())
        in_db.close()

        with open(data_list,'a') as L: # data_list : eg. 'train_lmdb_list.txt'
            L.write(os.path.realpath(lmdb_cur_path)+'\n')
