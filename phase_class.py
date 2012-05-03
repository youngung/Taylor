"""
A single phase's class
"""
class Phase:
    """
    """
    def __init__(self,
                 crystalstructure='fcc',
                 RVE=None,
                 gr=None,
                 discr_odf=None, ngr=None,
                 vf0=1.0,
                 crss0=1.0,
                 hardening='Voce',
        ):
        """
        """
        import cmb

        if RVE!=None: self.RVE = RVE
        elif gr!=None: self.RVE = RVE
        elif discr_odf!=None: self.RVE = cmb.RVE(
            ngrain=ngr, odf=descr_odf,
            cmbfile='temp.cmb')
        else:
            print 'Warning: texture is not given. '\
                'An RVE of 100 random grains is given'
            self.RVE = cmb.random(phi1=360, phi=90, phi2=180)
            #raise IOError
        self.ngr = len(self.RVE)

        self.crystalstructure = crystalstructure
        self.vf0 = vf0
        self.crss0 = crss0
        self.hardening = hardening

    def initialization(self):
        """
        """
        import numpy as np
        from gr_class import Grain        

        self.grains = [ ] 
        for i in range(len(self.RVE)):
            self.grains.append(
                Grain(structure = self.crystalstructure,
                      crss=self.crss0, euler=self.RVE[i][:3],
                      vf=self.RVE[i][-1],
                      hardeninglaw='Voce')
                )
        self.grains = np.array(self.grains)
