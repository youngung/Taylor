""" a grain's class
orientation, crss for slip systems and so on.
"""
class Grain:
    """
    """
    def __init__(
        self, structure='fcc', crss=1.0, euler=[0.,0.,0.], vf=1.0,
        hardeninglaw = 'Voce',
        ):
        """
        Grain initiallization
        """
        import numpy as np
        self.current_euler = euler # euler angle
        self.vf = vf
        self.current_acc_strain6 = np.zeros((3,3))
        self.current_stress6 = np.zeros((3,3))
        self.current_strain6_rate = np.zeros((3,3))
        self.current_temperature = 295. # Room temperature in K
        self.slipsystems = np.nan

        self.thermalcoeff = np.nan
        self.structure = structure
        self.crss = crss
        self.euler_trajectory = []
        self.euler_trajectory.append(euler)

        self.initialization()

    def initialization(self):
        """
        """
        import numpy as np
        self.__create_slipsystems__(self.structure)

    def __update_crss__(self):
        """ Slip system hardening law. (hardening)
        """
        for i in range(len(self.slipsystems)):
            pass

    def __update_ori__(self):
        """ Lattice rotation law. (Texture evolution)
        """

    def __create_slipsystems__(
        self, structure='fcc', crss=1.0, iopp=False
        ):
        """
        """
        import numpy as np
        import sym
        import lib

        structure=structure.lower()

        if structure=='fcc':
            sn = [[1,1,1]]
            sb = [[1,1,0]]
        elif structure=='bcc':
            # pencile glide with (1,1,0), (1,1,2),\
                # (1,2,3) planes.
            sn = [[1,1,0],[1,1,2],[1,2,3]]
            sb = [[1,1,1],[1,1,1],[1,1,1]]
        else: raise IOError, 'The structure is not'\
                'considered yet'

        ## multiplication of the direction and plane for
        ## the given structure
        if structure in ['fcc','bcc']:
            h = sym.cubic()
            slipsystems = []
            
            for i in range(len(sn)):
                normal = np.dot(h, sn[i])
                direc  = np.dot(h, sb[i])

                normal = lib.sort(normal, iopp=False)
                direc  = lib.sort(direc,  iopp=True)

                css = lib.sort_ss(sn=normal, sb=direc) # slip system
                slipsystems.append(css)

            self.slipsystems = slipsystems
        else: raise IOError, 'not ready yet!'

    def __rate_dependent_gamma__shear__(self):
        """
        """
