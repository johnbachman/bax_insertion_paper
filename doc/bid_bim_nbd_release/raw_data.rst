.. _bid_bim_terbium_nbd:

KD1: Bid/Bim Terbium and NBD Kinetics
=====================================

By measurement type
-------------------

.. plot::

    from bax_insertion.plots.nbd_bax_analysis import plot_all
    from bax_insertion.data.parse_bid_bim_nbd_release import df, nbd_residues
    plot_all(df, nbd_residues, ['Release', 'NBD'])

By replicate
------------

.. plot::

    from bax_insertion.plots.nbd_bax_analysis import plot_all_by_replicate
    from bax_insertion.data.parse_bid_bim_nbd_release import df, nbd_residues
    plot_all_by_replicate(df, nbd_residues, ['Release', 'NBD'])

