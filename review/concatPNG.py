# Concatenated mri images side by side for ingestion by pix2pix network 

import cv2
import numpy as np
import glob
import argparse 
import os

# parse cmd in
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dir', type=str)
opt = parser.parse_args()

# set vars 
c=0
ext = '.png'
files = glob.glob(opt.dir+'/*_t2_m*'+ext)
N=len(files)

for t2 in files:
	# find t2s file 
    t2s = t2.replace('_t2_m_tr', '_t2s_mcdc_m_hdr')
    # set output name 
    out = t2.replace('_t2_m_tr', '_t2_t2s_concat_')
    
    # read images
    img1 = cv2.imread(t2)
    img2 = cv2.imread(t2s)
    # concat 
    vis = np.concatenate((img1, img2), axis=1)
    # save
    cv2.imwrite(out, vis)
    # update and print counter
    c+=1
    print('%d / %d' % (c,N))
