import os
from glob import glob
from nipype.utils.filemanip import split_filename
from textwrap import dedent
from argparse import RawDescriptionHelpFormatter


def run_parser(subparsers):
    help = dedent("""
    Process subject-level data in fitz.

    This script controls the workflows that process data. Depending on the
    workflow, the data may start from raw DICOM or Nifti files and finish
    as processed models or group-level stats. See the documentation for the
    pipeline (collection of workflows) for information on exactly what the
    image inputs and outputs will be.

    All fitz workflows use Nipype, so there are several common options for
    efficiently running multiple subjects at once with differnt nipype plugins.
    The script can thus be run for several subjects at once, and (with a large
    enough cluster) all of the subjects can be processed in the time it takes
    to process a single run of data linearly.

    Nipype creates a cache directory to save processing time when steps are
    re-run. If you do not delete your cache directory after running (which is
    configured in the project file), repeated use of this script will only
    rerun the nodes that have changes to their inputs. Otherwise, you will
    have to rerun at the level of the workflows.


    Examples
    --------


    Note that the parameter switches match any unique short version
    of the full parameter name.

    fitz run -w xnatconvert preproc onset model

        Run every stage of the standar SPM fMRI pipeline for the default
        experiment for each subject defined in $FITZ_DIR/subjects.txt.
        The processing will be distributed locally with the MultiProc plugin
        using 4 processes.

    fitz run -s subj1 subj2 subj3 -w preproc

        Run preprocessing of the default experiment for subjects `subj1`,
        `subj2`, and `subj3`.

    fitz run -s pilot_subjects -w model -e nback -n 8

        Run the model workflow on the subjects enumerated in
        $FITZ_DIR/pilot_subjects.txt with the experiment details in
        $FITZ_DIR/nback.py. Distribute the execution locally with 8 parallel
        processes.

    Usage Details
    -------------

    """)
    if 'FITZ_DIR' in os.environ.keys():
        wf_files = glob(os.path.join(
            os.environ['FITZ_DIR'], '*/workflows/*.py'))
        workflows = [split_filename(wf)[1] for wf in wf_files]
    else:
        workflows = []
    parser = subparsers.add_parser('run', help='run')
    parser.description = help
    parser.formatter_class = RawDescriptionHelpFormatter
    parser.add_argument("--experiment", "-e", help="experimental paradigm")
    parser.add_argument("--model", "-m", help="model to fit")
    parser.add_argument("--workflows", "-w", nargs="*",
                        choices=workflows, help="which workflows to run")
    parser.add_argument("--subjects", "-s", nargs="*", dest="subjects",
                        help=("list of subject ids, name of file in lyman "
                              "directory, or full path to text file with "
                              "subject ids"))
    parser.add_argument("--plugin", "-p", default="multiproc",
                        choices=["linear", "multiproc", "ipython",
                                 "torque", "sge", "slurm"],
                        help="worklow execution plugin")
    parser.add_argument("--nprocs", "-n", default=4, type=int,
                        help="number of MultiProc processes to use")
    parser.add_argument("--queue", "-q", help="which queue for "
                                              "scheduler execution")
    parser.add_argument("--dontrun", action="store_true",
                        help="don't actually execute the workflows")
    return parser
