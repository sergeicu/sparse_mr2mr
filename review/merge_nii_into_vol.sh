#!/bin/bash

# fetch 13th slice (assuming that every predicted volume will have 13th slice)
for f in ${1}/*13.nii.gz
do 
	# identify base and output names 
	output="${f/0013/}"
	basename="${f/0013.nii.gz/}*"

	# merge 
	fslmerge -z $output $basename
done

example 
# di=/vol/medic02/users/sv407/my/ml/newdhcp/dhcp_fetch_test1/niftis/TEMP
# bash ./merge_nii_into_vol.sh $di/png2nifti/