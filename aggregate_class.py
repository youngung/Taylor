"""
gr - phase - Aggregate
"""
class Aggregate:
    """
    """
    def __init__(self,
                 nphase=1,

                 struct = ['fcc'],
                 RVE=[None],
                 gr=[None],
                 discr_odf=[None],
                 ngr=[None],
                 vf0 = [1.0],
                 crss0 = [1.0],
                 hardening = ['Voce']
                 ):
        """
        A phase has the same slip system characteristics,
        strain-hardening behavior, and so on.

        Arguments:
         nphase    = 1
         struct    = ['fcc']
         RVE       = [None]
         gr        = [None]
         discr_odf = [None]
         ngr       = [None]
         vf0       = [1.0]
         crss0     = [1.0]
         hardening = ['Voce']
        """
        import numpy as np
        # Volume fractioin normalization
        vf0 = np.array(vf0)
        vf0 = vf0/vf0.sum()
        # ------------------------------

        self.phases = []
        
        for i in range(nphase):
            ## characterization of the each phase.
            self.characterization(
                iphase = i, vf0 = vf0[i], struct = struct[i],
                RVE=RVE[i], gr=gr[i], discr_odf=discr_odf[i],
                ngr=ngr[i], crss0=crss0[i],
                hardening=hardening[i]
                )

    def characterization(
        self, iphase, vf0, struct,
        RVE, gr, discr_odf, ngr, crss0, hardening
        ):
        """
        How many phase?
        crystalline characteristics of each
        constituting phase

        And initialize the consitituent phases.
        """
        from phase_class import Phase
        self.phases.append(
            Phase(
                crystalstructure=struct,
                RVE = RVE,
                gr = gr,
                discr_odf = discr_odf,
                ngr=ngr,
                vf0=vf0,
                crss0=crss0,
                hardening=hardening
                ))
        self.phases[iphase].initialization()
            
        #
