import os
import glob
from shutil import copyfile

#compare dhcp2 (200 subjects) and dhcp3 (590 subjects) directories
base = '/vol/medic02/users/sv407/my/ml/newdhcp'
dhcp2 = glob.glob(base+'/dhcp_fetch_test2/niftis/*.nii.gz')
dhcp3 = glob.glob(base+'/dhcp_fetch_test3/*.nii.gz')
dhcp2_f = [os.path.basename(f) for f in dhcp2]
dhcp3_f = [os.path.basename(f) for f in dhcp3]

#unique files that are not in dhcp2 (200 subjects)
#matches = set(dhcp2_f).symmetric_difference(dhcp3_f)
unique = [f for f in dhcp3_f if f not in dhcp2_f]

[copyfile(os.path.join(base,'dhcp_fetch_test3',f), os.path.join(base,'dhcp_fetch_test4',f)) for f in unique]