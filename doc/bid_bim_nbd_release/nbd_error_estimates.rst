Estimates of error in NBD curves
================================

.. plot::

    from bax_insertion.data.parse_bid_bim_nbd_release import df, nbd_residues
    from bax_insertion.plots.nbd_bax_analysis import plot_nbd_error_estimates
    plot_nbd_error_estimates(df, nbd_residues, last_n_pts=80, fit_type='cubic')

