#!/bin/bash

for f in ${1}/*.nii.gz; do fslsplit $f ${f::-7} -z ; done;
#for f in ${1}/*.nii.gz; do fslsplit $f `dirname "$f"`/`basename "$f"` -z ; done;
