import glob 
import nibabel as nib
import cv2
import argparse 

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--nifti_dir', type=str)
opt = parser.parse_args()

c=0

for nifti in glob.glob(opt.nifti_dir+str('/*.nii.gz')):
    #def save path 
    path_png = nifti.replace(".nii.gz",".png")
    # load nifti 
    nii = nib.load(nifti)
    # extract array 
    nii_a = nii.get_fdata().round()
    # normalize 
    nii_a_n = cv2.normalize(nii_a, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX)
    # cast to uint8 
    nii_a_n_uint8 = nii_a_n.astype('uint8')
    # save as png
    cv2.imwrite(path_png, nii_a_n_uint8)
    #print & update counter 
    print('Image %d processed' % c)
    c+=1
