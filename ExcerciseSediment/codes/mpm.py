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

        # Use tau_x and tau_xcr in the Parker-Wong formula
        self.phi_b_pw = self.calculate_bedload()

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
        self.tau_x = self.compute_tau_x()
        try:
            difference = 0.85 * self.tau_x - self.tau_xcr

            if difference >= 0:  # Ensure the value is non-negative before raising to fractional power
                self.phi = 8 * difference ** (3 / 2)
            else:
                self.phi = np.nan  # Set phi to NaN or handle the case as needed

        except TypeError:
            logging.warning("Could not calculate PHI (result=%s)." % str(self.tau_x))
            self.phi = np.nan  # Default to NaN in case of errors

    def calculate_bedload(self):
        """
        Calculate the corrected bedload transport rate using the Parker-Wong formula:
        phi_b,pw = 4.93 * (tau_x - tau_xcr)^1.6
        """
        if self.tau_x > self.tau_xcr:
            # Apply Parker-Wong correction formula
            bedload_transport = 4.93 * (self.tau_x - self.tau_xcr) ** 1.6


            if bedload_transport < 0.1:
                logging.warning(f"Bedload transport is less with: {bedload_transport:.4f}")
            elif bedload_transport > 0.1 and bedload_transport < 1.0:
                logging.warning(f"Bedload transport is moderate with: {bedload_transport:.4f}")
            elif bedload_transport > 1.0:
                logging.warning(f"Bedload transport is huge with: {bedload_transport:.4f}")

        else:
            # No transport if shear stress is less than the critical shear stress
            bedload_transport = 0
            #logging.warning(f"tau_x und tau_xcr: {self.tau_x, self.tau_xcr}")
            logging.warning("Flow is to weak -> No bedload transport; tau_x <= tau_xcr.")
        return bedload_transport
