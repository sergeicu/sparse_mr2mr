'''
File name:
Author: github.com/sergeicu
Date created: 07/05/2019
Date last modified: 07/05/2019

Matching names of junyaz-pix2pix model image inference results (in .nii.gz) with the DHCP database equivalent nifti slices.
The output is used for splicing 3D nifti files together and comparing the inferred volume to original ground truth.
'''

import os
import glob
from shutil import copyfile
import argparse

# parse inputs
parser = argparse.ArgumentParser()
parser.add_argument('--results_dir', type=str, default='/vol/medic02/users/sv407/my/ml/junyaz-p2p/results/dhcp2_basic_7400/test_latest/images')
parser.add_argument('--nifti_dir', type=str, default='/vol/medic02/users/sv407/my/ml/newdhcp/dhcp_fetch_test4/niftis_as_slices')
opt = parser.parse_args()

# fetch generated images (image inferences for T2S slices)
fakes = glob.glob(opt.results_dir+'/*fake*.png')

# change file names to match with those of original nifti slices
fakes_match = []
for f in fakes:
    # n, e = os.path.splitext(f)
    b = os.path.basename(f)
    b = b.replace('t2_t2s_concat_', 't2s_mcdc_m_hdr')
    b = b.replace('_fake_B', '')
    fakes_match.append(b)

#create directory for holding fakes images that are of the same name as nifti slices
os.makedirs(os.path.join(opt.results_dir,'name_match_to_original_niis'),exist_ok=True)

check=True
if check:
    # check if the newly named images match with original .nii.gz slices
    nii = fakes_match[1].replace('png', 'nii.gz') # do a single check (extend if necessary)
    nii_fp = os.path.join(opt.nifti_dir,nii)
    print('original image name: \n\t%s' % os.path.basename(fakes[1]))
    print('new image name: \n\t%s' % fakes_match[1])
    print('results_dir: \n\t%s' % opt.results_dir)
    print('nifti_dir to search: \n\t%s' % opt.nifti_dir)
    print('does the new image name match to original nifti slice?')
    print('\t%s' % os.path.isfile(nii_fp))

else:
    for src,dest in zip(fakes,fakes_match):
        src_fp = os.path.join(opt.results_dir, src)
        dest_fp = os.path.join(opt.results_dir,'name_match_to_original_niis',dest)
        copyfile(src_fp, dest_fp)

