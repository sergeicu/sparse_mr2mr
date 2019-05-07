# Applies random shuffles to a directory of files and sorts them into train/test/val directories 

import shutil 
from glob import glob
import random
import argparse 
import os 

def main():
	# parse cmd in
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--input_dir', type=str)
	parser.add_argument('--ext', type=str)
	args = parser.parse_args()

	#create directories 
	for d in ['trainA','testA','valA','trainB','testB','valB']:
	    os.makedirs('%s/%s' % (args.input_dir, d), exist_ok=True)

	#fetch all files 
	files = glob('%s/*t2_m_*%s' % (args.input_dir, args.ext))


	#define split ratio
	val_size = 200
	test_size = 200 
	train_size = len(files)-val_size-test_size

	# check if train dir has enough files 
	check_train_size(train_size)

	#select random train files 
	index = random.sample(range(0,len(files)), train_size)
	to_sendA = [files[i] for i in index]
	to_sendB = [f.replace("t2_m_tr", "t2s_mcdc_m_hdr") for f in to_sendA]


	[shutil.move(f, args.input_dir+'/trainA/') for f in to_sendA]
	[shutil.move(f, args.input_dir+'/trainB/') for f in to_sendB]


	# NB there is more elegant way to do this, but we'll do a quick hack 

	# fetch remaining files       
	files = glob('%s/*t2_m_*%s' % (args.input_dir, args.ext))

	#select random test files 
	index = random.sample(range(0,len(files)), test_size)
	to_sendA = [files[i] for i in index]
	to_sendB = [f.replace("t2_m_tr", "t2s_mcdc_m_hdr") for f in to_sendA]

	# send to test dir 
	[shutil.move(f, args.input_dir+'/testA/') for f in to_sendA]
	[shutil.move(f, args.input_dir+'/testB/') for f in to_sendB]

	# fetch & move the remaining files to val dir 
	filesA = glob('%s/*t2_m_*%s' % (args.input_dir, args.ext))
	filesB = glob('%s/*t2s_mcdc_m_*%s' % (args.input_dir, args.ext))
	[shutil.move(f, args.input_dir+'/valA/') for f in filesA]
	[shutil.move(f, args.input_dir+'/valB/') for f in filesB]


def check_train_size(train_size):
    if train_size <200:
        raise Exception('Training size is smaller than validation and test sizes. Please change sizes')

if __name__ == '__main__':
    main()
