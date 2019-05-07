#!/bin/bash
 
# prints out all subjectid and sessionid for subjects that possess both a T2 and T2* file 
# masks t2 and t2s images, aligns them to each other, resamples and rotates them to match each other 
 
savedir=/vol/medic02/users/sv407/my/ml/newdhcp/dhcp_fetch_test3
t2sdir=/vol/dhcp-results/neofmri_2nd_release_rerun2
t2dir=/vol/dhcp-derived-data/derived_02Jun2018/derivatives
allt2files=${t2dir}/sub-*/ses-*/anat/sub-*_ses*T2w_restore.nii.gz
c=0
L=20000
for t2 in ${allt2files};  
do  
    # extract subject ID and session IDs 
    subid=$(echo $t2 | egrep -o 'sub-[a-zA-Z]+[0-9]+[a-zA-Z]+[0-9]+/'); 
    sesid=$(echo $t2 | egrep -o 'ses-[0-9]+/'); 
    subid=${subid:0:-1}
    sesid=${sesid:0:-1}
    t2s=${t2sdir}/${subid}/${sesid}/fix/func_clean_mean.nii.gz
    if [ -f $t2s ] && [ $c -lt $L ]; then 

        c=$[$c+1]
        echo "subject $c out of $L" 
        echo $t2s

        #savename
        savename=${savedir}/${subid}_${sesid}
        
        # mask t2s and t2 
        t2_mask=${t2dir}/${subid}/${sesid}/anat/${subid}_${sesid}_brainmask_bet.nii.gz
        t2s_mask=${t2sdir}/${subid}/${sesid}/mcdc/func_mcdc_brainmask.nii.gz
        padding $t2s $t2s_mask ${savename}_t2s_mcdc_m.nii.gz 0 1
        padding $t2 $t2_mask ${savename}_t2_m.nii.gz 0 1
        
        # align t2 and t2s
        headertool ${savename}_t2s_mcdc_m.nii.gz ${savename}_t2s_mcdc_m_hdr.nii.gz -targetOriginAndOrient ${savename}_t2_m.nii.gz
        
        # resample t2 to match t2s
        transformation ${savename}_t2_m.nii.gz  ${savename}_t2_m_tr.nii.gz  -target ${savename}_t2s_mcdc_m_hdr.nii.gz -sinc

        # remove intermediate files 
        rm ${savename}_t2s_mcdc_m.nii.gz ${savename}_t2_m.nii.gz

    fi;  
done; 


 
