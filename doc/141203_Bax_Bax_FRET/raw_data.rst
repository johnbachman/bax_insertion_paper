Raw data
========

By measurement type
-------------------

.. plot::

    from bax_insertion.plots.nbd_bax_analysis import plot_all
    from bax_insertion.plots.x141203_Bax_Bax_FRET.preprocess_data \
            import df, nbd_residues
    plot_all(df, nbd_residues, ['Release', 'NBD', 'FRET'], activators=['Bid'],
             replicates=(1,))

By replicate
------------

.. plot::

    from bax_insertion.plots.nbd_bax_analysis import plot_all_by_replicate
    from bax_insertion.plots.x141203_Bax_Bax_FRET.preprocess_data \
            import df, nbd_residues
    plot_all_by_replicate(df, nbd_residues, ['Release', 'NBD', 'FRET'],
                          activators=['Bid'], replicates=(1,))

