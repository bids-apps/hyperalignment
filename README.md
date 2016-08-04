## Hyperalignment BIDS App (WiP)

This App has the following common line arguments:

		usage: run.py [-h]
		              [--participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]
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

Participant level mode prepares the data for hyperalignment.
For now, it loads the data into PyMVPA readable datasets.
In future, this will be modified to compute individual subject connectomes.

    docker run -i --rm -v /Users/swaroop/ds005-deriv-3subjects/derivatives:/bids_dataset \
        -v /Users/swaroop/outputs:/outputs \
        hyperalignment \
        /bids_dataset /outputs participant --task mixedgamblestask --run 01

After doing this for all subjects (potentially in parallel) the group level analysis
runs hyperalignment and saves transformation parameters.

    docker run -i --rm -v /Users/swaroop/ds005-deriv-3subjects/derivatives:/bids_dataset \
        -v /Users/swaroop/outputs:/outputs \
        hyperalignment \
        /bids_dataset /outputs group

