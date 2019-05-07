import os 
import glob 
import cv2
import argparse 
import skimage.measure as skm
import csv
import datetime
import numpy as np




def main(): 
    # Suppress scientific notation (e.g. 423.2234e+04)
    np.set_printoptions(suppress=True)

    #setup parser
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--testdir', type=str)
    opt = parser.parse_args()

    # select only folders within the checkpoints directory
    dirs = [ name for name in os.listdir(opt.testdir) if os.path.isdir(os.path.join(opt.testdir,name)) ]

    #time now 
    t_now = datetime.datetime.now().strftime('%m%d-%H%M')
    #savename
    f4 = os.path.join(opt.testdir,'im_compare_metrics_all_%s.csv' % (t_now)) 
    #def file to write to 
    with open(f4,'a') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(['MSE, NRMSE, SSIM, PSNR, test_name'])
        
        # compare images in each directory 
        for d in dirs:
            print(d)
            img_metrics = compare_images(os.path.join(opt.testdir, d, 'test_latest/images' ))
            writer.writerow([img_metrics, d])
        file.close()
        


def compare_images(img_dir):


    t_now = datetime.datetime.now().strftime('%m%d-%H%M')
    f1 = os.path.join(img_dir,'im_compare_metrics_%s.csv' % (t_now))
    f2 = os.path.join(img_dir,'im_compare_names_%s.csv' % (t_now))
    f3 = os.path.join(img_dir,'im_compare_metrics_average_%s.csv' % (t_now))

    #obsolete
    #print('\nMetrics saved to: \n\n%s' % (f1))
    #print('\nCorresponding file names saved to: \n\n%s' % (f2))

    ext = '.png'

    #fetch list of images from input pathA directory 
    images = glob.glob(img_dir + '/*real_B%s' % (ext))

    all_m = []

    for A in images: 
        m = [None]*4
        #A_path, A_file = os.path.split(A)
        B = A.replace('real_B', 'fake_B')
        A_im = cv2.imread(A)
        B_im = cv2.imread(B)
        m[0] = round(skm.compare_mse(A_im, B_im),0)
        m[1] = round(skm.compare_nrmse(A_im, B_im),2)
        m[2] = round(skm.compare_ssim(A_im, B_im, multichannel=True),2)
        m[3] = round(skm.compare_psnr(A_im, B_im),2)
        names = [os.path.basename(A), os.path.basename(B)]
        all_m.append(m)

#only enable if need to write intermediate results for each individual image in each test directory
#        write2file(m,names,f1,f2) 
    
    #for debug only
    #print(f3)
    #print(np.round(np.mean(all_m,0),2))


    img_metrics = np.round(np.mean(all_m,0),2)
#only enable if need to write intermediate results in each test directory
#    with open(f3,'a') as file:
#        writer = csv.writer(file)
#        writer.writerow(['MSE, NRMSE, SSIM, PSNR for %d images' % len(images)])
#        writer.writerow(img_metrics)
#        file.close()

    return img_metrics  
    

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
    main()

# Run test as: 
# cd my 
# python compare_imgs_junyaz_gan.py --testdir /vol/medic02/users/sv407/my/ml/junyaz-p2p/results/facades_label2photo_pretrained/test_latest/images

# Run LPIPS test as: 
# cd my 
# python compute_dists_dirs.py --dir0 /vol/medic02/users/sv407/my/ml/Keras-GAN/cyclegan/datasets/facades/testA/ --dir1 /vol/medic02/users/sv407/my/ml/Keras-GAN/cyclegan/datasets/facades/testB/