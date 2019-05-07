import glob 
import nibabel as nib
import cv2
import argparse 
import os 
import errno


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--nifti_dir', type=str)
parser.add_argument('--png_dir', type=str)
opt = parser.parse_args()

unmatched_files = []
for i, png in enumerate(glob.glob(opt.png_dir+str('/*.png'))):
	# find equivalent nifti image
	d, f = os.path.split(png)
	r, e = os.path.splitext(f)
	nifti = os.path.join(opt.nifti_dir, r+str('.nii.gz'))
	# if exists, save to nifti 
	if os.path.isfile(nifti):
		# load original slice 
		nii = nib.load(nifti)
		#def save path 
		path_nii = png.replace(".png", ".nii.gz")
		# load png
		im = cv2.imread(png)
		# cast to float 
		im_float64 = im.astype('float64')
		# cut to 1 axis only (all channels equal)
		im_float64_1dim = im_float64[:,:,0]
		# convert to nifti 
		nii_from_png = nib.Nifti1Image(im_float64_1dim,nii.affine,header=nii.header) 
		nii_from_png.to_filename(path_nii)
	else:
		# else throw exception
		#raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), nifti)
		unmatched_files.append(nifti)
	print(i)
print('unmatched files:')
for f in unmatched_files:
	print(f)

# example 
# di=/vol/medic02/users/sv407/my/ml/newdhcp/dhcp_fetch_test1/niftis/TEMP
# python png2nii.py --nifti_dir $di/nifti --png_dir $di/png
