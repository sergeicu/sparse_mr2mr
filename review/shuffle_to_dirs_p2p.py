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
	for d in ['train','test','val']:
	    os.makedirs('%s/%s' % (args.input_dir, d), exist_ok=True)

	#fetch all files 
	files = glob('%s/*%s' % (args.input_dir, args.ext))


	#define split ratio
	val_size = 200
	test_size = 200 
	train_size = len(files)-val_size-test_size

	# check if train dir has enough files 
	check_train_size(train_size)

	#select random train files 
	index = random.sample(range(0,len(files)), train_size)
	to_send = [files[i] for i in index]

	#move files to train dir 
	[shutil.move(f, args.input_dir+'/train/') for f in to_send]

	# NB there is more elegant way to do this, but we'll do a quick hack 

	# fetch remaining files       
	files = glob('%s/*%s' % (args.input_dir, args.ext))

	#select random test files 
	index = random.sample(range(0,len(files)), test_size)
	to_send = [files[i] for i in index]

	# send to test dir 
	[shutil.move(f, args.input_dir+'/test/') for f in to_send]

	# fetch & move the remaining files to val dir 
	files = glob('%s/*%s' % (args.input_dir, args.ext))
	[shutil.move(f, args.input_dir+'/val/') for f in files]


def check_train_size(train_size):
    if train_size <200:
        raise Exception('Training size is smaller than validation and test sizes. Please change sizes')

if __name__ == '__main__':
    main()