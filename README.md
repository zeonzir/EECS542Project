# EECS542Project
Visual odometry project
Updates in inverse chronological order
- Sigmoid and Euclidean loss fails, converting from stacked input to split input (left channel has labels)
- After 40K iterations training loss not right, beginning to debug
- Discussed baseline 3 and 4 network structures
- Training started
- Design of network architecture complete (Baseline 2)
- Design of network architecture complete (Baseline 1)
- Pre-processing data into stack images for HDF5 and 3 labels
- Created 2 format converters HDF5 and LMDB
- Going over KITTI dataset and trying to massage it into required form for training
- Basic ingredients for training learnt, from tutorial
- Recompiled caffe with cuDNN (solved missing cuDNN issue, copied into correct folder cuda-7.5)
- Installed caffe - without cuDNN (compilation issues)
- Project proposal submitted
