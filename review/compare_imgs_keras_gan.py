import os 
import glob 
import cv2
import argparse 
import skimage.measure as skm
import csv
import datetime
import numpy as np

def compare_images():

    #setup parser
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--pathA', type=str)
    parser.add_argument('--pathB', type=str)
    opt = parser.parse_args()

    t_now = datetime.datetime.now().strftime('%m%d-%H%M')
    f1 = os.path.join(opt.pathA,'im_compare_metrics_%s.csv' % (t_now))
    f2 = os.path.join(opt.pathA,'im_compare_names_%s.csv' % (t_now))
    f3 = os.path.join(opt.pathA,'im_compare_metrics_average_%s.csv' % (t_now))

    print('\nMetrics saved to: \n\n%s' % (f1))
    print('\nCorresponding file names saved to: \n\n%s' % (f2))

    ext = '.jpg'

    #fetch list of images from input pathA directory 
    images = glob.glob(opt.pathA + '/*%s' % (ext))

    all_m = []

    for A in images: 
        m = [None]*4
        A_path, A_file = os.path.split(A)
        B = os.path.join(opt.pathB + A_file)
        A_im = cv2.imread(A)
        B_im = cv2.imread(B)
        m[0] = round(skm.compare_mse(A_im, B_im),0)
        m[1] = round(skm.compare_nrmse(A_im, B_im),2)
        m[2] = round(skm.compare_ssim(A_im, B_im, multichannel=True),2)
        m[3] = round(skm.compare_psnr(A_im, B_im),2)
        names = [A_file, os.path.basename(B)]
        write2file(m,names,f1,f2)
        all_m.append(m)

    with open(f3,'a') as file:
        writer = csv.writer(file)
        writer.writerow(['MSE, NRMSE, SSIM, PSNR for %d images' % len(images)])
        writer.writerow(np.round(np.mean(all_m,0),2))
        file.close()

def write2file(metrics, names,f1,f2):
    
    with open(f1, 'a') as file1: 
        writer = csv.writer(file1)
        writer.writerow(metrics)
    file1.close()
    
    with open(f2, 'a') as file2:  
        writer = csv.writer(file2)
        writer.writerow(names)
    file2.close()

if __name__ == '__main__':
    compare_images()

# Run test as: 
# cd my 
# python compare_imgs.py --pathA /vol/medic02/users/sv407/my/ml/Keras-GAN/cyclegan/datasets/facades/testA/ --pathB /vol/medic02/users/sv407/my/ml/Keras-GAN/cyclegan/datasets/facades/testB/

# Run LPIPS test as: 
# cd my 
# python compute_dists_dirs.py --dir0 /vol/medic02/users/sv407/my/ml/Keras-GAN/cyclegan/datasets/facades/testA/ --dir1 /vol/medic02/users/sv407/my/ml/Keras-GAN/cyclegan/datasets/facades/testB/