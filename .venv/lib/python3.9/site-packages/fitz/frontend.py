"""Forward facing fitz tools with information about ecosystem."""
import os
import re
import sys
import imp
import os.path as op
import numpy as np
import subprocess
from nipype import config, logging
from .tools import make_subject_source


def gather_project_info():
    """Import project information based on environment settings."""
    fitz_dir = os.environ["FITZ_DIR"]
    proj_file = op.join(fitz_dir, "project.py")
    try:
        project = sys.modules["project"]
    except KeyError:
        project = imp.load_source("project", proj_file)

    project_dict = dict()
    for dir in ["data", "analysis", "working", "crash"]:
        path = op.abspath(op.join(fitz_dir, getattr(project, dir + "_dir")))
        project_dict[dir + "_dir"] = path
    project_dict["default_exp"] = project.default_exp
    project_dict["rm_working_dir"] = project.rm_working_dir

    if hasattr(project, "ants_normalization"):
        use_ants = project.ants_normalization
        project_dict["normalization"] = "ants" if use_ants else "fsl"
    else:
        project_dict["normalization"] = "fsl"

    return project_dict


def gather_experiment_info(exp_name=None, model=None):
    """Import an experiment module and add some formatted information."""
    fitz_dir = os.environ["FITZ_DIR"]

    # Allow easy use of default experiment
    if exp_name is None:
        project = gather_project_info()
        exp_name = project["default_exp"]

    # Import the base experiment
    try:
        exp = sys.modules[exp_name]
    except KeyError:
        exp_file = op.join(fitz_dir, exp_name + ".py")
        exp = imp.load_source(exp_name, exp_file)

    exp_dict = {}

    def keep(k):
        return not re.match("__.*__", k)

    exp_dict.update({k: v for k, v in exp.__dict__.items() if keep(k)})

    # Possibly import the alternate model details
    if model is not None:
        check_modelname(model, exp_name)
        try:
            mod = sys.modules[model]
        except KeyError:
            model_file = op.join(fitz_dir, "%s-%s.py" % (exp_name, model))
            mod = imp.load_source(model, model_file)

        mod_dict = {k: v for k, v in mod.__dict__.items() if keep(k)}

        # Update the base information with the altmodel info
        exp_dict.update(mod_dict)

    # Save the __doc__ attribute to the dict
    exp_dict["comments"] = "" if exp.__doc__ is None else exp.__doc__
    if model is not None:
        exp_dict["comments"] += "" if mod.__doc__ is None else mod.__doc__

    do_lyman_tweaks(exp_dict)

    return exp_dict


def do_lyman_tweaks(exp_dict):
    # Check if it looks like this is a partial FOV acquisition
    exp_dict["partial_brain"] = bool(exp_dict.get("whole_brain_template"))

    # Temporal resolution.
    if "TR" in exp_dict.keys():
        exp_dict["TR"] = float(exp_dict["TR"])

    # Set up the default contrasts
    if ("condition_names" in exp_dict.keys() and
            exp_dict["condition_names"] is not None):
        cs = [(name, [name], [1]) for name in exp_dict["condition_names"]]
        exp_dict["contrasts"] = cs + exp_dict["contrasts"]

    if "contrast_names" in exp_dict.keys():
        # Build contrasts list if neccesary
        exp_dict["contrast_names"] = [c[0] for c in exp_dict["contrasts"]]


def determine_subjects(subject_arg=None):
    """Intelligently find a list of subjects in a variety of ways."""
    if subject_arg is None:
        subject_file = op.join(os.environ["FITZ_DIR"], "subjects.txt")
        subjects = np.loadtxt(subject_file, str, ndmin=1).tolist()
    elif op.isfile(subject_arg[0]):
        subjects = np.loadtxt(subject_arg[0], str).tolist()
    else:
        try:
            subject_file = op.join(os.environ["FITZ_DIR"],
                                   subject_arg[0] + ".txt")
            subjects = np.loadtxt(subject_file, str).tolist()
        except IOError:
            subjects = subject_arg
    return subjects


def determine_engine(args):
    """Read command line args and return Workflow.run() args."""
    plugin_dict = dict(linear="Linear", multiproc="MultiProc",
                       ipython="IPython", torque="PBS", sge="SGE",
                       slurm="SLURM")

    plugin = plugin_dict[args.plugin]

    plugin_args = dict()
    qsub_args = ""

    if plugin == "MultiProc":
        plugin_args['n_procs'] = args.nprocs
    elif plugin in ["SGE", "PBS"]:
        qsub_args += "-V -e /dev/null -o /dev/null "

    if args.queue is not None:
        qsub_args += "-q %s " % args.queue

    plugin_args["qsub_args"] = qsub_args

    return plugin, plugin_args


def update_params(wf_module, exp):
    # print sys.path, dir(wf_module), wf_module.__name__, wf_module.__file__
    try:
        params = wf_module.default_parameters
    except IOError:
        print "Workflow must define a default_parameters method!"
        raise

    # default_names = set(params.keys())
    params.update(exp)
    # current_names = set(params.keys())
    # print default_names, current_names

    # new_names = current_names - default_names
    # print new_names
    # if len(new_names):
    #     msg = ["You may have an invalid configuration:"]
    #     for name in new_names:
    #         msg.append("A value for %s was specified, " % name +
    #                    "but not expected by the workflow")
    #     raise Exception(msg)
    return params


def check_modelname(model, exp_name):
    """Do Some sanity checks on the model"""
    err = []
    if model.endswith('.py'):
        err.append("Don't include '.py' when listing your model. ")
    if model.startswith(exp_name):
        err.append("Don't include the experiment name (%s) " % exp_name +
                   "when listing your model.")
    if len(err):
        err.insert(0, "Problem with the way you specified your model on " +
                      "the commandline:")
        raise IOError('\n- '.join(err))


def run(args):
    """Get and process specific information"""
    project = gather_project_info()
    exp = gather_experiment_info(args.experiment, args.model)

    # Subject is always highest level of parameterization
    subject_list = determine_subjects(args.subjects)
    subj_source = make_subject_source(subject_list)

    # Get the full correct name for the experiment
    if args.experiment is None:
        exp_name = project["default_exp"]
    else:
        exp_name = args.experiment

    exp['exp_name'] = exp_name
    exp['model_name'] = args.model if args.model else ''

    # Set roots of output storage
    project['analysis_dir'] = op.join(project["analysis_dir"], exp_name)
    project['working_dir'] = op.join(project["working_dir"], exp_name,
                                     exp['model_name'])

    config.set("execution", "crashdump_dir", project["crash_dir"])
    if args.verbose > 0:
        config.set("logging", "filemanip_level", 'DEBUG')
        config.enable_debug_mode()
        logging.update_logging(config)

    if not op.exists(project['analysis_dir']):
        os.makedirs(project['analysis_dir'])

    workflows_dir = os.path.join(os.environ['FITZ_DIR'], exp['pipeline'],
                                 'workflows')
    if not op.isdir(workflows_dir):
        missing_pipe = 'raise'
        if missing_pipe == 'install':
            install(args)
        else:
            raise IOError("Run `fitz install` to set up your pipeline of "
                          "workflows, %s does not exist." % workflows_dir)
    sys.path.insert(0, workflows_dir)
    for wf_name in args.workflows:
        try:
            mod = imp.find_module(wf_name)
            wf_module = imp.load_module("wf", *mod)
        except (IOError, ImportError):
            print "Could not find any workflows matching %s" % wf_name
            raise

        params = update_params(wf_module, exp)
        workflow = wf_module.workflow_manager(
            project, params, args, subj_source)

        # Run the pipeline
        plugin, plugin_args = determine_engine(args)
        workflow.write_graph(str(workflow)+'.dot', format='svg')
        if not args.dontrun:
            workflow.run(plugin, plugin_args)


def install(args):
    project = gather_project_info()
    exp = gather_experiment_info(project['default_exp'])

    cmd = ['git', 'clone', exp['pipeline_src']]
    workflow_base = os.path.splitext(os.path.basename(exp['pipeline_src']))[0]
    print workflow_base
    print ' '.join(cmd)
    if not os.path.isdir(workflow_base):
        subprocess.check_call(cmd)
    else:
        print "Workflow %s already exists." % workflow_base

    cmd = ['git', 'checkout', exp['pipeline_version']]
    print ' '.join(cmd)
    try:
        subprocess.check_call(cmd, cwd=workflow_base)
    except:
        print "Error checking out tag %s" % exp['pipeline_version']
        # raise
