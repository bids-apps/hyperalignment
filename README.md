## Hyperalignment BIDS App (WiP)

### Description
Hyperalignment is a functional alignment method that aligns subjects' brain data in a 
high-dimensional space of voxels/features. We showed that this alignment aligns subjects 
at a fine-scale affording between-subject decoding and encoding 
[Guntupalli et al. 2016](http://cercor.oxfordjournals.org/content/26/6/2919). This app runs searchlight
hyperalignment, which runs hyperalignment in multiple searchlights across the whole brain and
aggregates them into a single transformation per subject.
For now, many parameters such as searchlight size, sparsity of centers, etc., are fixed.
Please use PyMVPA to modify these and other parameters for your use case.

### Documentation
For a detailed documentation and examples, please see:  
Hyperalignment in a ROI:  
http://www.pymvpa.org/generated/mvpa2.algorithms.hyperalignment.Hyperalignment.html  
Searchlight Hyperalignment:  
https://github.com/PyMVPA/PyMVPA/blob/master/mvpa2/algorithms/searchlight_hyperalignment.py  
Example in PyMVPA:  
http://www.pymvpa.org/examples/hyperalignment.html  

### Acknowledgements
If you use this in your project, please cite [Guntupalli et al. 2016](http://cercor.oxfordjournals.org/content/26/6/2919).

### Report Bugs/Issues
Please use PyMVPA on github to report any bugs/issues or to contribute:
https://github.com/PyMVPA/PyMVPA

### Usage

		usage: run.py [-h]
		              [--participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...] 
		              --task TASK_LABEL --run RUN_LABEL]
		              bids_dir output_dir {participant,group}

		Example BIDS App entrypoint script.

		positional arguments:
		  bids_dir              The directory with the input dataset formatted
		                        according to the BIDS standard.
		  output_dir            The directory where the output files should be stored.
		                        If you are running group level analysis this folder
		                        should be prepopulated with the results of
		                        theparticipant level analysis.
		  {participant,group}   Level of the analysis that will be performed. Multiple
		                        participant level analyses can be run independently
		                        (in parallel).

		optional arguments:
		  -h, --help            show this help message and exit
		  --participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]
		                        The label(s) of the participant(s) that should be
		                        analyzed. The label corresponds to
		                        sub-<participant_label> from the BIDS spec (so it does
		                        not include "sub-"). If this parameter is not provided
		                        all subjects should be analyzed. Multiple participants
		                        can be specified with a space separated list.
		  --task TASK_LABEL     Name of the task that should be used for hyperalignment.
		                        This correspnds to task-<TASK_LABEL> from the BIDS spec 
		                        (so it does not include "task-").
		  --run RUN_LABEL       Name of the run that should be used for hyperalignment.
		                        This correspnds to run-<TASK_LABEL> from the BIDS spec 
		                        (so it does not include "run-").


Participant level mode prepares the data for hyperalignment.
For now, it loads the data from nifti image into PyMVPA readable datasets after applying
brain mask. In future, this will be modified to compute individual subject connectomes.

    docker run -i --rm \
        -v /Users/swaroop/ds005-deriv/derivatives:/bids_dataset \
        -v /Users/swaroop/outputs:/outputs \
        bids/hyperalignment \
        /bids_dataset /outputs participant \
        --task mixedgamblestask --run 01 --participant_label 01

After running participant level (potentially in parallel), group level analysis
runs hyperalignment and saves transformation parameters.

    docker run -i --rm -v \
        /Users/swaroop/ds005-deriv/derivatives:/bids_dataset \
        -v /Users/swaroop/outputs:/outputs \
        bids/hyperalignment \
        /bids_dataset /outputs group

### Special requirements
Hyperalignment works on preprocessed data with all the subjects' data aligned to the same template.

### Relevant references:  
1. Guntupalli, J. S., Hanke, M., Halchenko, Y. O., Connolly, A. C., Ramadge, P. J. & Haxby, J. V. (2016). A Model of Representational Spaces in Human Cortex. Cerebral Cortex.
    DOI: http://dx.doi.org/10.1093/cercor/bhw068  
2. Haxby, J. V., Guntupalli, J. S., Connolly, A. C., Halchenko, Y. O., Conroy, B. R., Gobbini, M. I., Hanke, M. & Ramadge, P. J. (2011). A Common, High-Dimensional Model of the Representational Space in Human Ventral Temporal Cortex. Neuron, 72, 404–416.
    DOI: http://dx.doi.org/10.1016/j.neuron.2011.08.026  
