.. _bid_bim_fret_terbium_nbd:

KD2: Bid/Bim FRET, NBD, and Release Kinetics
============================================

By measurement type
-------------------

.. plot::

    from bax_insertion.plots.nbd_bax_analysis import plot_all
    from bax_insertion.data.parse_bid_bim_fret_nbd_release import df, nbd_residues
    plot_all(df, nbd_residues, ['Release', 'NBD', 'FRET'])

By replicate
------------

.. plot::

    from bax_insertion.plots.nbd_bax_analysis import plot_all_by_replicate
    from bax_insertion.data.parse_bid_bim_fret_nbd_release import df, nbd_residues
    plot_all_by_replicate(df, nbd_residues, ['Release', 'NBD', 'FRET'])

