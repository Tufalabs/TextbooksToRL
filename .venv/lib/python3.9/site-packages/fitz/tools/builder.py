import os


def new_workflow(args):
    template_name = 'workflow_template.py'
    readme_name = 'README.rst'
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    pipe_dir = os.path.join(os.environ['FITZ_DIR'], args.pipe_name)
    pipe_wf_dir = os.path.join(pipe_dir, 'workflows')
    template_args = vars(args).copy()

    # Setup Dirs
    if not os.path.isdir(pipe_wf_dir):
        os.makedirs(pipe_wf_dir)

    # Setup Reame
    readme_src = os.path.join(templates_dir, readme_name)
    readme_dest = os.path.join(pipe_dir, readme_name)
    if not os.path.exists(readme_dest):
        copytemplate(readme_src, readme_dest, template_args)

    # Setup Workflow
    workflow_template = os.path.join(templates_dir, template_name)
    workflow_dest = os.path.join(pipe_wf_dir, args.workflow_name + '.py')
    if os.path.exists(workflow_dest):
        raise IOError('Workflow %s already exists! ' % (workflow_dest) +
                      'Please delete it and run again if you meant to ' +
                      'overwrite it.')
    else:
        copytemplate(workflow_template, workflow_dest, template_args)
        print 'Created new template workflow: %s' % workflow_dest


def copytemplate(src, dest, args):
    """Write a source template to a new file and interpolate args."""
    with open(src) as t:
        template = t.read()
    with open(dest, 'w') as d:
        d.write(template.format(**args))
