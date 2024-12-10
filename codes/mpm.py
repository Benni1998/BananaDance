from bedload import *
import logging
import numpy as np

class MPM(BedCore):
    def __init__(self, grain_size, Froude, water_depth,
                 velocity, Q, hydraulic_radius, slope):
        # initialize parent class
        BedCore.__init__(self)
        # assign parameters from arguments
        self.D = grain_size
        self.h = water_depth
        self.Q = Q
        self.Se = slope
        self.Rh = hydraulic_radius
        self.u = velocity
        self.check_validity(Froude)
        self.compute_phi()

    def check_validity(self, Fr):
        if (self.Se < 0.0004) or (self.Se > 0.02):
            logging.warning('Warning: Slope out of validity range.')
        if (self.D < 0.0004) or (self.D > 0.0286):
            logging.warning('Warning: Grain size out of validity range.')
        if ((self.u * self.h) < 0.002) or ((self.u * self.h) > 2.0):
            logging.warning('Warning: Discharge out of validity range.')
        if (self.s < 0.25) or (self.s > 3.2):
            logging.warning('Warning: Relative grain density (s) out of validity range.')
        if (Fr < 0.0001) or (Fr > 639):
            logging.warning('Warning: Froude number out of validity range.')

    def compute_phi(self):
        tau_x = self.compute_tau_x()
        try:
            difference = 0.85 * tau_x - self.tau_xcr

            if difference >= 0:  # Ensure the value is non-negative before raising to fractional power
                self.phi = 8 * difference ** (3 / 2)
            else:
                self.phi = np.nan  # Set phi to NaN or handle the case as needed

        except TypeError:
            logging.warning("Could not calculate PHI (result=%s)." % str(tau_x))
            self.phi = np.nan  # Default to NaN in case of errors