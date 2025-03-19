#!/usr/bin/env python
# Create Lyman/Fitz style long flat Design Files from plain-text onset files
# EKK / June 2015
# Python 2/3 compatibile, depends on Pandas and Numpy/Scipy

from __future__ import print_function
from pandas import concat, read_csv
from argparse import ArgumentParser, FileType
from numpy import empty


def main(args):
    runs_df = load_onsets(args.onsets_files, args)
    print("Saving designfile (%d rows) to %s" % (runs_df.shape[0], args.out))
    runs_df.to_csv(args.out, index=False)


def load_onsets(onsets_files, args):
    """Read onsets file and add metadata from their filenames.
    Return one concatenated pandas dataframe with all trials as rows."""
    runs = []
    for i, fid in enumerate(onsets_files):
        run = read_csv(fid)

        # If any column arguments were given, convert to a lyman-like design
        # with explicitly named columns. Else, just concatenate and add 'run'.
        if (args.onset_col or args.duration_col or args.condition_col or
                args.pmods_col):
            run = rename_columns(args, run)
            condition_col = 'condition'
            # Remove blanks
            run = run[run[condition_col].notnull()]

        # Add fn and run to designfile
        run['filename'] = fid.name
        if 'run' not in run.columns:
            run['run'] = i + 1

        # Drop any columns thar are entirely empty (for vanity)
        for col_name, col in run.iteritems():
            if col.isnull().all():
                del(run[col_name])

        runs.append(run)

    return concat(runs, ignore_index=True)


def rename_columns(args, run):
    cols = ['run', 'onset', 'duration', 'condition']

    # Cleanup any columns that might exist if we don't want them
    if args.drop_cols:
        for col in cols:
            if col in run.columns:
                run.drop(col, axis=1, inplace=True)

    columns = {}

    columns[args.onset_col] = 'onset'
    columns[args.condition_col] = 'condition'

    if args.run_col:
        columns[args.run_col] = 'run'

    if args.duration_col:
        columns[args.duration_col] = 'duration'
    else:
        run['duration'] = 0

    if len(args.pmods_col):
        for pmod in args.pmods_col:
            columns[pmod] = 'pmod-' + pmod
            cols.append('pmod-' + pmod)

    run.rename(columns=columns, inplace=True)

    return run[cols]


def onsets_for(cond, run_df):
    """
    Inputs:
      * Condition Label to grab onsets, durations & amplitudes for.
      * Pandas Dataframe for current run containing onsets values as columns.

    Outputs:
      * Returns a dictionary of extracted values for onsets, durations, etc.
      * Returns None if there are no onsets.
    """
    condinfo = {}
    cond_df = run_df[run_df['condition'] == cond]

    if cond_df['onset'].notnull().any():  # Onsets Present
        if cond_df['duration'].notnull().any():
            durations = cond_df['duration'].tolist()
        else:
            durations = [0]

        condinfo = dict(
            name=cond,
            durations=durations,
            onsets=cond_df['onset'].tolist(),
        )

        if ('amplitude' in cond_df.columns and
                cond_df['amplitude'].notnull().any()):
            pmods = [dict(
                name=args.pmod_name,
                poly=1,
                param=cond_df['amplitude'].tolist(),
            )]
            condinfo['pmod'] = pmods
    else:
        condinfo = None
    return condinfo


def _lists_to_scipy(onsets_list):
    """
    Inputs:
      * List of dicts (one dict for each condition)

        [{'name':'Low','durations':0,'onsets':[1,3,5]},
         {'name':'Hi', 'durations':0, 'onsets':[2,4,6]}]

        - Or with Parametric Modulators -
        [{'name':'Low','durations':0,'onsets':[1,3,5], 'pmod':[
           {'name': 'RT', 'poly':1, 'param':[42,13,666]}]},
         {'name':'High',, 'durations':0, 'onsets':[2,4,6]}]

    Outputs:
      * Dict of scipy arrays for keys names, durations and onsets
        that can be written using scipy.io.savemat
    """

    conditions_n = len(onsets_list)
    names = empty((conditions_n,),     dtype='object')
    durations = empty((conditions_n,), dtype='object')
    onsets = empty((conditions_n,),    dtype='object')

    pmoddt = [('name', 'O'), ('poly', 'O'), ('param', 'O')]
    pmods = empty((conditions_n),      dtype=pmoddt)
    has_pmods = False

    for i, ons in enumerate(onsets_list):
        names[i] = ons['name']
        durations[i] = ons['durations']
        onsets[i] = ons['onsets']
        if 'pmod' not in ons.keys():
            pmods[i]['name'], pmods[i]['poly'], pmods[i]['param'] = [], [], []
        else:
            # 'pmod': [{'name':'rt','poly':1,'param':[1,2,3]}]
            # Multiple pmods per condition are allowed, so pmod
            # is a list of dicts.
            has_pmods = True
            cond_pmod_list = ons['pmod']
            current_condition_n_pmods = len(cond_pmod_list)
            pmod_names = empty((current_condition_n_pmods,), dtype='object')
            pmod_param = empty((current_condition_n_pmods,), dtype='object')
            pmod_poly = empty((current_condition_n_pmods,), dtype='object')

            for pmod_i, val in enumerate(cond_pmod_list):
                pmod_names[pmod_i] = val['name']
                pmod_param[pmod_i] = val['param']
                pmod_poly[pmod_i] = float(val['poly'])

            pmods[i]['name'] = pmod_names
            pmods[i]['poly'] = pmod_poly
            pmods[i]['param'] = pmod_param

    scipy_onsets = dict(
        names=names,
        durations=durations,
        onsets=onsets
    )

    if has_pmods:
        scipy_onsets['pmod'] = pmods

    return scipy_onsets


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('onsets_files', type=FileType('r'),
                        help='List of FSL EV onsets to convert', nargs='+')
    parser.add_argument('--out',   '-o', default='onsets_',
                        help='Output filename.')
    parser.add_argument('--verbose',      '-v', action="count",
                        help="increase output verbosity")
    parser.add_argument('--pmod-name', default='pmod',
                        help='Name to use when writing FSL Amplitude as SPM '
                             'parametric modulator')
    parser.add_argument('--conditions', '-c', default=[], nargs='+')
    parser.add_argument('--condition-col')
    parser.add_argument('--duration-col')
    parser.add_argument('--onset-col', default='')
    parser.add_argument('--pmods-col', default=[], nargs="*")
    parser.add_argument('--run-col')
    parser.add_argument('--drop-cols', help='Drop pre-named columns in'
                                            'longform',
                        default=True)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    if args.verbose >= 2:
        print(args)
    main(args)
