import re
import sys
import pickle
import os.path

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
    with open(filename, 'rb') as f:
        (gf, sampler) = pickle.load(f)

    # Get the maximum a posteriori parameters
    maxp_flat_ix = np.argmax(sampler.lnprobability[0])
    maxp_ix = np.unravel_index(maxp_flat_ix,
                               sampler.lnprobability[0].shape)
    maxp = sampler.lnprobability[0][maxp_ix]
    # Store the tuple in a dict
    #file_dict[(prefix, residue, repnum)] = arr
    return (prefix, residue, repnum, maxp)

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
    for filename in filelist[6:7]:
        cd = get_curve_data(filename)
        curve_data.append(cd)

