.. _bax_bax_fret_terbium_nbd:

KD3: Bax-Bax FRET, NBD, and Release Kinetics
============================================

By measurement type
-------------------

.. plot::

    from bax_insertion.plots.nbd_bax_analysis import plot_all
    from bax_insertion.data.parse_bax_bax_fret_nbd_release import df, nbd_residues
    plot_all(df, nbd_residues, ['Release', 'NBD', 'FRET'], activators=['Bid'])

By replicate
------------

.. plot::

    from bax_insertion.plots.nbd_bax_analysis import plot_all_by_replicate
    from bax_insertion.data.parse_bax_bax_fret_nbd_release import df, nbd_residues
    plot_all_by_replicate(df, nbd_residues, ['Release', 'NBD', 'FRET'], activators=['Bid'])

