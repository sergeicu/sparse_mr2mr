
import os
import glob
import cv2
import argparse
import nibabel as nib
from subprocess import run
from shutil import move

def main(opt):
    # fetch list of nii files
    #nii_paths = glob.glob(opt.nifti_dir + '/*.nii.gz')
    nii_paths = glob.glob(opt + '/*.nii.gz')

    # load gan
    #GAN = load_gan(opt.gan_model)
    GAN = load_gan('')

    # process each nii separately
    for nii_path in nii_paths:
        nii_s_paths = split_to_slices(nii_path)
        nii_s_fake_paths = []
        for nii_s_path in nii_s_paths:
            # convert nifti to png
            png_path, nii_obj = nii_to_png(nii_s_path)
            #translate image with pre-trained GAN
            png_path_fake = im2im_translate(png_path)
            #convert new png back to nifti
            nii_s_fake_path = png_to_nii(png_path_fake, nii_obj)
            #collect intermediate slices for later removal
            nii_s_fake_paths.append(nii_s_fake_path)
        #merge all individual slices to single volume
        merge_to_vol(nii_path)
        # cleanup
        cleanup(nii_s_fake_paths, nii_s_paths)
        # calculate img comparison metrics


# load model
def load_gan(gan_model):
    pass

# split into slices 
def split_to_slices(nii_path):
    nii_basename = nii_path[:-7]
    run(["fslsplit", nii_path, nii_basename, "-z"])
    nii_s_paths = glob.glob(nii_basename + '[0-9]*.nii.gz')
    return nii_s_paths

# convert into jpg
def nii_to_png(nii_s_path):
    # load nifti
    nii = nib.load(nii_s_path)
    # extract array
    nii_a = nii.get_fdata().round()
    # normalize
    nii_a_n = cv2.normalize(nii_a, None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX)
    # cast to uint8
    nii_a_n_uint8 = nii_a_n.astype('uint8')
    # save as png
    png_path = nii_s_path.replace(".nii.gz",".png")
    cv2.imwrite(png_path, nii_a_n_uint8)
    return png_path, nii

# predict using the saved model
def im2im_translate(png_file):
    # load png
    im = cv2.imread(png_file,0)
    # save png
    savename = png_file.replace(".png", "_fake_t2s.png")
    cv2.imwrite(savename, im)
    #return png_translated_file
    return savename

# turn back into nii
def png_to_nii(png_path_fake, nii_obj):

    # load png
    im = cv2.imread(png_path_fake,0)
    # cast to float
    im_float64 = im.astype('float64')
    # convert to nifti
    nii_from_png = nib.Nifti1Image(im_float64, nii_obj.affine, header=nii_obj.header)
    # save file
    path_nii = png_path_fake.replace(".png",".nii.gz")
    nii_from_png.to_filename(path_nii)
    return path_nii

# fuse into vol
def merge_to_vol(nii_slices):
    nii_slices_basename = nii_slices[:-(7 + 2)] + '*[0-9]*fake_t2s.nii.gz'
    output_name = nii_slices[:-7]+'_fake_t2s.nii.gz'
    cmd = ["fslmerge", "-z", output_name, nii_slices_basename]
    os.system(" ".join(cmd))

def cleanup(nii_s_paths, nii_s_fake_paths):
    # remove all nii slices to conserve space
    # note that we keep all PNG files as they may be required for later processing (e.g. img metric comparisons, etc)
    for f1, f2 in zip(nii_s_paths, nii_s_fake_paths):
        os.remove(f1)
        os.remove(f2)
    # move png files to separate dir
    pngs = glob.glob(opt + '/*.png')
    png_dir = '%s/%s' % (opt, 'png')
    os.makedirs(png_dir, exist_ok=True)
    [move(png, png_dir) for png in pngs]
    # move translated files to separate dir
    nii_fake = glob.glob(opt + '/*_fake_t2s.nii.gz')
    nii_fake_dir = '%s/%s' % (opt, 'fake_t2s')
    os.makedirs(nii_fake_dir, exist_ok=True)
    [move(nii, nii_fake_dir) for nii in nii_fake]


# [optional] calculate image difference between original and new (on slice by slice basis)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--nifti_dir', type=str)
    parser.add_argument('--gan_model', type=str)
    opt = parser.parse_args()
    opt ='/vol/medic02/users/sv407/my/ml/code_playground/20190502_python_subprocesses'
    main(opt)