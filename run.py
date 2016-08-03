#!/usr/bin/env python
import argparse
import os
import subprocess
import nibabel
import numpy as np
from glob import glob
from mvpa2.suite import *
from mvpa2.base.hdf5 import h5save, h5load
from mvpa2.algorithms.searchlight_hyperalignment import SearchlightHyperalignment
from mvpa2.datasets.mri import fmri_dataset
from mvpa2.mappers.zscore import zscore


parser = argparse.ArgumentParser(description='Example BIDS App entrypoint script.')
parser.add_argument('bids_dir', help='The directory with the input dataset '
                                     'formatted according to the BIDS standard.')
parser.add_argument('output_dir', help='The directory where the output files '
                                       'should be stored. If you are running group level analysis '
                                       'this folder should be prepopulated with the results of the'
                                       'participant level analysis.')
parser.add_argument('analysis_level',
                    help='Level of the analysis that will be performed. '
                         'Multiple participant level analyses can be run independently '
                         '(in parallel) using the same output_dir.',
                    choices=['participant', 'group'])
parser.add_argument('--participant_label',
                    help='The label(s) of the participant(s) that should be analyzed. The label '
                         'corresponds to sub-<participant_label> from the BIDS spec '
                         '(so it does not include "sub-"). If this parameter is not '
                         'provided all subjects should be analyzed. Multiple '
                         'participants can be specified with a space separated list.',
                    nargs="+")
parser.add_argument('--task',
                    help='Task from which the data is used for deriving hyperalignment '
                          'parameters')
parser.add_argument('--run',
                    help='Run or runs to be used for deriving hyperalignment parameters')

args = parser.parse_args()

subjects_to_analyze = []
# only for a subset of subjects
if args.participant_label:
    subjects_to_analyze = args.participant_label
# for all subjects
else:
    subject_dirs = glob(os.path.join(args.bids_dir, "sub-*"))
    subjects_to_analyze = [subject_dir.split("-")[-1] for subject_dir in subject_dirs]

"""
At the participant level, load nifti data using mask and store it as hdf5 file.
This can be adapted to compute connectomes later.
"""


def prepare_subject_for_hyperalignment(subject_label, bold_fname, mask_fname, out_dir):
    print('Loading data %s with mask %s' % (bold_fname, mask_fname))
    ds = fmri_dataset(samples=bold_fname, mask=mask_fname)
    zscore(ds, chunks_attr=None)
    out_fname = os.path.join(out_dir, 'sub-%s_data.hdf5' % subject_label)
    print('Saving to %s' % out_fname)
    h5save(out_fname, ds)


def run_hyperalignment(subjects_to_analyze, out_dir):
    # Load subject data
    ds_all = []
    for subject_label in subjects_to_analyze:
        ds_all.append(h5load('%s/sub-%s_data.hdf5' % (out_dir, subject_label)))
    # Initialize searchlight hyperalignment
    slhyper = SearchlightHyperalignment(radius=2, nblocks=10, sparse_radius=5,
                                         dtype='float16')
    hmappers = slhyper(ds_all)
    return hmappers


# This can be subject-level and be applied in parallel
def apply_hyperalignment():
    raise NotImplementedError


"""
Helper functions to save and load mappers
"""


def save_mappers(hmappers, fname):
    h5save(fname, hmappers)


def load_mappers(fname):
    return h5load(fname)

# running participant level

if args.analysis_level == "participant":
    # sub-01_task-mixedgamblestask_run-02_bold_hmc_mni.nii.gz
    prefixes = []
    task_prefix = 'task-%s' % args.task
    prefixes.append(task_prefix)
    run_prefix = 'run-%s' % args.run
    prefixes.append(run_prefix)
    # XXX TODO Expose this option outside?
    preproc_prefix = 'bold_hmc_mni'
    prefixes.append(preproc_prefix)
    # find all T1s and skullstrip them
    prefix = '_'.join(prefixes)
    for subject_label in subjects_to_analyze:
        bold_fname = 'sub-%s_%s'%(subject_label, prefix)
        bold_fname = os.path.join(args.bids_dir, "sub-%s" % subject_label,
                                  "func", bold_fname)
        mask_fname = '%s_bmask.nii.gz' % bold_fname
        bold_fname = '%s.nii.gz' % bold_fname
        prepare_subject_for_hyperalignment(subject_label, bold_fname, mask_fname,
                                           args.output_dir)

# running group level
elif args.analysis_level == "group":
    """
    Load data (timeseries or connectomes) stored in first-level
    and run hyperalignment. Spit out mappers.
    """
    hmappers = run_hyperalignment(subjects_to_analyze, out_dir=args.output_dir)
    hmappers_fname = os.path.join(args.output_dir, 'hmappers.hdf5')
    save_mappers(hmappers=hmappers, fname=hmappers_fname)
    with open(os.path.join(args.output_dir, "Transformation_matrix_shapes.txt"), 'w') as fp:
        for hm in hmappers:
        fp.write("Transformation shape and non-zero elements : " % hm.proj.shape, hm.proj.data.size)
