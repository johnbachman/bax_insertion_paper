import re
import sys
import pickle
import os.path
import numpy as np

filelist = [
    'bid_bim_nbd_release/mcmc_norm_prior/pt_data1_newpr_Bid_NBD_3_r1_3confs.mcmc',
    'bid_bim_nbd_release/mcmc_norm_prior/pt_data1_newpr_Bid_NBD_36_r1_3confs.mcmc',
    'bid_bim_nbd_release/mcmc_norm_prior/pt_data1_newpr_Bid_NBD_54_r1_3confs.mcmc',
    'bid_bim_nbd_release/mcmc_norm_prior/pt_data1_newpr_Bid_NBD_126_r1_3confs.mcmc',
    'bid_bim_nbd_release/mcmc_norm_prior/pt_data1_newpr_Bid_NBD_138_r1_3confs.mcmc',
    'bid_bim_nbd_release/mcmc_norm_prior/pt_data1_newpr_Bid_NBD_175_r1_3confs.mcmc',
    'bid_bim_fret_nbd_release/fret_mcmc_norm/pt_data2_fret_norm_Bid_NBD_3_r1_3confs.mcmc',
    'bid_bim_fret_nbd_release/fret_mcmc_norm/pt_data2_fret_norm_Bid_NBD_36_r1_3confs.mcmc',
    'bid_bim_fret_nbd_release/fret_mcmc_norm/pt_data2_fret_norm_Bid_NBD_54_r1_3confs.mcmc',
    'bid_bim_fret_nbd_release/fret_mcmc_norm/pt_data2_fret_norm_Bid_NBD_126_r1_3confs.mcmc',
    'bid_bim_fret_nbd_release/fret_mcmc_norm/pt_data2_fret_norm_Bid_NBD_138_r1_3confs.mcmc',
    'bid_bim_fret_nbd_release/fret_mcmc_norm/pt_data2_fret_norm_Bid_NBD_175_r1_3confs.mcmc',
    'bax_bax_fret_nbd_release/fret_mcmc_norm/pt_data3_fret_norm_Bid_NBD_3_r1_3confs.mcmc',
    'bax_bax_fret_nbd_release/fret_mcmc_norm/pt_data3_fret_norm_Bid_NBD_36_r1_3confs.mcmc',
    'bax_bax_fret_nbd_release/fret_mcmc_norm/pt_data3_fret_norm_Bid_NBD_54_r1_3confs.mcmc',
    'bax_bax_fret_nbd_release/fret_mcmc_norm/pt_data3_fret_norm_Bid_NBD_126_r1_3confs.mcmc',
    'bax_bax_fret_nbd_release/fret_mcmc_norm/pt_data3_fret_norm_Bid_NBD_138_r1_3confs.mcmc',
    'bax_bax_fret_nbd_release/fret_mcmc_norm/pt_data3_fret_norm_Bid_NBD_175_r1_3confs.mcmc',
    ]

def get_curve_data(filename):
    # First, split off the dirname
    basename = os.path.basename(filename)
    # Next, split off the extension(s)
    basename = basename.split('.')[0]
    pattern = re.compile('(\w+)_Bid_NBD_(\d+)_r(\d)_3confs')
    m = pattern.match(basename)
    if not m:
        raise Exception('Could not match filename %s' % basename)
    # Get the keys from the regex
    (prefix, residue, repnum) = m.groups()
    repnum = int(repnum)
    # Load the file
    print("Loading %s" % filename)
    with open(filename, 'rb') as f:
        (gf, sampler) = pickle.load(f)

    # Get the maximum a posteriori parameters
    maxp_flat_ix = np.argmax(sampler.lnprobability[0])
    maxp_ix = np.unravel_index(maxp_flat_ix,
                               sampler.lnprobability[0].shape)
    maxp = sampler.lnprobability[0][maxp_ix]
    param_names = [p.name for p in gf.builder.estimate_params]
    maxp_params = sampler.chain[0, maxp_ix[0], maxp_ix[1]]
    param_tuples = list(zip(param_names, maxp_params))
    # Store the tuple in a dict
    #file_dict[(prefix, residue, repnum)] = arr
    return (prefix, residue, repnum, param_tuples)

if __name__ == '__main__':
    #filelist = sys.argv[1:]
    missing_file = False
    for file in filelist:
        if not os.path.exists(file):
            print("Error: file %s does not exist" % file)
            #missing_file = True
    if missing_file:
        sys.exit(1)

    # Get the curve data for each file
    curve_data = []
    for filename in filelist[0:2]:
        cd = get_curve_data(filename)
        curve_data.append(cd)

    # Prepare data rows for export
    rows = []
    labels = {
        'pt_data1_newpr': 'KD1',
        'pt_data2_fret_norm': 'KD2',
        'pt_data3_fret_norm': 'KD3',
    }
    for prefix, residue, repnum, param_tuples in curve_data:
        for p_name, p_val in param_tuples:
            p_val_lin = 10**p_val
            row = [labels[prefix], residue, repnum, p_name, p_val_lin]
    with open('fig5_MAP_parameter_table.csv', 'w') as f:
        csvwriter = csv.writer(f, delimiter=',')
        csvwriter.writerows(rows)

