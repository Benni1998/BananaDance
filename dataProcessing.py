import subprocess

import matplotlib.pyplot as plt
import numpy as np
import re
import pandas as pd

from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MultipleLocator
#from config import FILE_PATH, CREATE_PICTURES, LIMIT_DATA, LIMIT

class DataExtractor:
    """
    Extracts and organizes sections of data from a log file based on "STOP" delimiters.
    """

    def __init__(self, file_path):
        """
        Initializes the extractor with a file path.

        :param file_path: Path to the log file.
        """
        self.file_path = file_path

    def __call__(self):
        """
        Extracts sections from the file and returns them.

        :return: List of sections, where each section is a list of strings (lines).
        """
        return self.extract_sections()

    def extract_sections(self):
        """
        Reads the file and splits its content into sections based on "STOP" markers.

        :return: List of sections, each containing lines from the file.
        """
        sections = []
        current_section = []

        with open(self.file_path, 'r') as file:
            for line in file:
                if "STOP" in line:
                    sections.append(current_section)
                    current_section = []
                else:
                    current_section.append(line)

        if current_section:
            sections.append(current_section)

        return sections

class Calculation:
    """
    Processes sections to extract valid particles and calculates relevant metrics.
    """

    def __call__(self, section):
        """
        Extracts valid particle data from a section.

        Args:
            section (list): List of strings representing lines from a section.

        Returns:
            np.ndarray: Array of valid particle data.
        """
        return self.extract_valid_particles(section)

    def extract_valid_particles(self, section):
        """
        Filters and parses valid particles from the section.

        Args:
            section (list): List of lines to analyze.

        Returns:
            np.ndarray: Array containing valid particles with attributes [Y, Z, Velocity, XS].
        """
        valid_particles = [self.parse_line(line) for line in section if "LogBlueprintUserMessages" in line]
        return np.array([particle for particle in valid_particles if particle])

    def parse_line(self, line):
        """
        Parses a line to extract valid particle data.

        Args:
            line (str): String containing particle data.

        Returns:
            list or None: [Y, Z, Velocity, XS] if valid, otherwise None.
        """
        key_match = re.search(r'KEY: \d+', line)
        vector_match = re.search(r'VECTOR: X=[-.\d]+ Y=[-.\d]+ Z=[-.\d]+', line)
        velocity_match = re.search(r'VELOCITY: [-.\d]+', line)
        xs_match = re.search(r"XS(\d+)", line)

        if key_match and vector_match and velocity_match and xs_match:
            y, z = self.extract_vector_components(line)
            velocity = self.extract_velocity(line)
            xs_value = int(xs_match.group(1))
            return [y, z, velocity, xs_value]
        return None

    def extract_vector_components(self, line):
        """
        Extracts Y and Z components from a vector string.

        Args:
            line (str): String containing vector information.

        Returns:
            tuple: (Y, Z) values as floats.
        """
        y_match = re.search(r'Y=([-\d.]+)', line)
        z_match = re.search(r'Z=([-\d.]+)', line)
        return float(y_match.group(1)) / 100, float(z_match.group(1)) / 100

    def extract_velocity(self, line):
        """
        Extracts velocity value from a line.

        Args:
            line (str): String containing velocity information.

        Returns:
            float: Velocity value.
        """
        velocity_match = re.search(r'VELOCITY: [-.\d]+', line)
        return round(float(velocity_match.group(0).split(": ")[1]) / 100, 3)

    def calculate_average_velocity(self, data):
        """
        Calculates the average velocity of particles.

        Args:
            data (np.ndarray): Array of particle data with velocities in the 3rd column.

        Returns:
            float: Average velocity rounded to 3 decimal places.
        """
        return round(np.mean(data[:, 2]), 3) if data.size > 0 else 0

    def calculate_standard_deviation(self, data):
        """
        Calculates the standard deviation of particle velocities.

        Args:
            data (np.ndarray): Array of particle data with velocities in the 3rd column.

        Returns:
            float: Standard deviation rounded to 3 decimal places.
        """
        return round(np.std(data[:, 2]), 3) if data.size > 0 else 0

    def calculate_average_particle_count(self, sections):
        """
        Calculates the average number of particles for each cross-section (XS).

        Args:
            sections (list): List of sections containing particle data.

        Returns:
            dict: Dictionary with average particle counts for each XS category.
        """
        # Initialize totals and counts for each XS
        xs_totals = {11: 0, 41: 0, 21: 0, 31: 0, 12: 0, 42: 0, 22: 0, 32: 0}
        xs_counts = {11: 0, 41: 0, 21: 0, 31: 0, 12: 0, 42: 0, 22: 0, 32: 0}

        for section_number, section in enumerate(sections, start=1):
            # Process each section to update totals and counts
            data = self.extract_valid_particles(section)
            valid_particle_count = len(data)

            if valid_particle_count > 0:
                xs_key = self._determine_xs(data, section_number)
                if xs_key in xs_totals:
                    xs_totals[xs_key] += valid_particle_count
                    xs_counts[xs_key] += 1

        # Calculate averages
        xs_averages = {}
        for xs_key in xs_totals:
            if xs_counts[xs_key] > 0:
                xs_averages[xs_key] = round(xs_totals[xs_key] / xs_counts[xs_key], 1)
            else:
                xs_averages[xs_key] = 0

        return xs_averages

    def _process_section(self, section, section_number, xs_totals, xs_counts):
        """
        Processes a single section and updates totals and counts for XS categories.

        Args:
            section (list): Lines in the section.
            section_number (int): The current section number.
            xs_totals (dict): Dictionary to store total particle counts for each XS.
            xs_counts (dict): Dictionary to store image counts for each XS.
        """
        data = self.extract_valid_particles(section)
        valid_particle_count = len(data)

        if valid_particle_count > 0:
            xs_key = self._determine_xs(data, section_number)
            if xs_key:
                xs_totals[xs_key] += valid_particle_count
                xs_counts[xs_key] += 1

    def _determine_xs(self, data, section_number):
        """
        Determines the cross-section (XS) key based on data and section number.

        Args:
            data (np.ndarray): Particle data array.
            section_number (int): The current section number.

        Returns:
            int or None: XS key (e.g., 11, 41) or None if no match is found.
        """
        xs_value = int(data[:, 3].mean())  # Get the XS value
        if xs_value == 1:
            return 11 if section_number < 20 else 12
        elif xs_value == 4:
            return 41 if section_number < 40 else 42
        elif xs_value == 2:
            return 21 if section_number < 50 else 22
        elif xs_value == 3:
            return 31 if section_number < 60 else 32
        return None

    def _calculate_averages(self, xs_totals, xs_counts):
        """
        Calculates average particle counts for each XS category.

        Args:
            xs_totals (dict): Total particle counts for each XS.
            xs_counts (dict): Image counts for each XS.

        Returns:
            list: Average particle counts for each XS category.
        """
        return [
            round(xs_totals[xs] / xs_counts[xs], 1) if xs_counts[xs] > 0 else 0
            for xs in [11, 41, 21, 31, 12, 42, 22, 32]
        ]


class Plotter:
    """
    Generates scatter plots visualizing particle data.
    """

    def __call__(self, data, avg_particles, sd_velocity, valid_particle_count, avg_velocity, section_number, xlim_left, xlim_right):
        """
        Creates a plot for the given particle data.

        :param data: NumPy array of particle data.
        :param avg_particles: Average particle count across sections.
        :param sd_velocity: Standard deviation of velocity.
        :param valid_particle_count: Count of valid particles.
        :param avg_velocity: Average velocity of particles.
        :param section_number: Section number being processed.
        """
        self.plot_data(data, avg_particles, sd_velocity, valid_particle_count, avg_velocity, section_number,xlim_left, xlim_right)

    @staticmethod
    def create_custom_cmap():
        """
        Creates a custom rainbow colormap.

        :return: LinearSegmentedColormap object.
        """
        colors = [
            (0.0, (0, 0, 0.5)),
            (0.125, (0, 0, 1.0)),
            (0.375, (0, 1.0, 1.0)),
            (0.5, (0, 1.0, 0)),
            (0.625, (1.0, 1.0, 0)),
            (0.875, (1.0, 0, 0)),
            (1.0, (0.5, 0, 0))
        ]
        return LinearSegmentedColormap.from_list('custom_rainbow', colors)

    def plot_data(self, data, avg_particles, sd_velocity, valid_particle_count, avg_velocity, section_number,xlim_left, xlim_right):
        """
        Creates and saves a scatter plot for the data.

        :param data: NumPy array of particle data.
        :param avg_particles: Average particle count across sections.
        :param sd_velocity: Standard deviation of velocity.
        :param valid_particle_count: Count of valid particles.
        :param avg_velocity: Average velocity of particles.
        :param section_number: Section number being processed.
        """
        fig, ax_scatter, ax_colorbar = self.setup_figure()
        self.create_scatter_plot(ax_scatter, data, xlim_left, xlim_right)
        self.add_colorbar(fig, ax_colorbar, data)
        self.add_titles(fig, valid_particle_count, avg_particles, avg_velocity, sd_velocity, section_number)
        self.save_plot(fig, section_number)

    def setup_figure(self):
        """
        Sets up the figure and axes for plotting.

        :return: Tuple (Figure, scatter axis, colorbar axis).
        """
        fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
        gs = GridSpec(2, 1, height_ratios=[0.1, 0.9])
        return fig, fig.add_subplot(gs[1]), fig.add_subplot(gs[0])

    def create_scatter_plot(self, ax, data, xlim_left, xlim_right):
        """
        Plots the scatter plot for particle data.

        :param ax: Matplotlib Axes object for scatter plot.
        :param data: NumPy array of particle data.
        """
        Y, Z, velocity = data[:, 0], data[:, 1], data[:, 2]
        cmap = self.create_custom_cmap()
        ax.scatter(Y, Z, c=velocity, cmap=cmap, vmin=0, vmax=2, alpha=1.0, s=np.pi * (0.1 * 10) ** 2)
        ax.set_facecolor('white')
        ax.set_xlabel('Y Values (m)', fontsize=18)
        ax.set_ylabel('Z Values (m)', fontsize=18)
        ax.yaxis.set_major_locator(MultipleLocator(0.01))
        ax.grid(True, which='both', linestyle='--', color='gray', linewidth=0.7)
        ax.set_ylim(0, 0.8)
        ax.set_xlim(xlim_left, xlim_right)
        ax.tick_params(labelsize=10)

    def reduce_particles(self, data, limit):
        """
        Filters out particles with velocities below the specified limit.

        Args:
            data (np.ndarray): Array of particle data with attributes [Y, Z, Velocity, XS].
            limit (float): Minimum velocity threshold. Particles with velocities below this value are removed.

        Returns:
            np.ndarray: Filtered array containing only particles with velocities >= limit.
        """
        if data.size == 0:
            return data  # Return the original array if empty

        # Use boolean indexing to filter particles
        reduced_data = data[data[:, 2] >= limit]
        return reduced_data

    def add_colorbar(self, fig, ax, data):
        """
        Adds a colorbar to the plot.

        :param fig: Matplotlib Figure object.
        :param ax: Matplotlib Axes object for colorbar.
        :param data: NumPy array of particle data.
        """
        scatter = fig.axes[0].collections[0]
        cbar = fig.colorbar(scatter, cax=ax, orientation='horizontal', pad=0.0)
        cbar.set_label('Velocity (m/s)', fontsize=18, labelpad=10)
        cbar.ax.xaxis.set_label_position('top')
        cbar.ax.tick_params(labelsize=8)

    def add_titles(self, fig, count, avg_particle, avg_velocity, sd_velocity, section_number):
        """
        Adds titles to the plot.

        Args:
            fig (matplotlib.figure.Figure): Matplotlib figure object.
            count (int): Number of valid particles.
            avg_particle (float): Average particle count for the current XS.
            avg_velocity (float): Average velocity of particles.
            sd_velocity (float): Standard deviation of velocity.
            section_number (int): Section number being processed.
        """
        fig.suptitle(f'Section {section_number} Results\n'
                     f'Particles: {count}, Average particles: {avg_particle},\n'
                     f'Average velocity: {avg_velocity:.3f} m/s, sd velocity: {sd_velocity:.3f}',
                     fontsize=18, y=0.01)

    def save_plot(self, fig, section_number):
        """
        Saves the plot as a PNG file.

        :param fig: Matplotlib Figure object.
        :param section_number: Section number for naming the file.
        """
        output_filename = f'section_plot_{section_number}.png'
        plt.savefig(output_filename, format='png', bbox_inches='tight')
        plt.close()

class Main:
    """
    Main driver class to process the log file, analyze sections, and generate plots.
    """

    def __init__(self, file_path):
        """
        Initializes the main class with the file path.

        :param file_path: Path to the log file.
        """

        self.xs_limits = {
            11: (-1.1, 1.3), 12: (-1.1, 1.3),  # XS 1.1 and 1.2
            21: (-2.4, 1.4), 22: (-2.4, 1.4),  # XS 2.1 and 2.2
            31: (-2.4, 1.4), 32: (-2.4, 1.4),  # XS 3.1 and 3.2
            41: (-1.4, 1.3), 42: (-1.4, 1.3)  # XS 4.1 and 4.2
        }

        self.file_path = file_path
        self.data_list = []

    def __call__(self):
        """
        Processes the file and generates plots for each section.
        """

        self.create_pictures = True
        self.limit_Data = False
        self.limit = 0.03

        extractor = DataExtractor(self.file_path)
        calculation = Calculation()
        plotter = Plotter()

        sections = extractor()

        # Calculate average particle counts using the new method
        avg_particles = calculation.calculate_average_particle_count(sections)


        # Process each section and generate plots
        for section_number, section in enumerate(sections, start=1):
           self.process_section(section, calculation, plotter, avg_particles, section_number)

        df = pd.DataFrame(self.data_list)

        df_sorted = df.sort_values(by=['sd_velocity'], ascending=False)
        mean_value = df['sd_velocity'].mean()
        df.to_csv('Values.csv', index=False)
        print(df.head(5))
        print("mean sd_velocity: " + str(mean_value))
        print(df_sorted.head(5))


    def process_section(self, section, calculation, plotter, avg_particles, section_number):
        """
        Processes a single section of data.

        Args:
            section (list): List of strings representing the section.
            calculation (Calculation): Instance of the Calculation class.
            plotter (Plotter): Instance of the Plotter class.
            avg_particles (list): Average particle count across sections.
            section_number (int): Section number being processed.
        """


        data = calculation(section)
        valid_particle_count = len(data)
        avg_velocity = calculation.calculate_average_velocity(data)
        sd_velocity = calculation.calculate_standard_deviation(data)

        rows = []

        if valid_particle_count > 0:
            # Determine the XS for the current section
            current_xs = calculation._determine_xs(data, section_number)
            left_value, right_value = self.xs_limits.get(current_xs)
            avg_particle = avg_particles.get(current_xs, 0)  # Fetch the correct average for the current XS

            print(f'Section {section_number}: Anzahl der gültigen Partikel: {valid_particle_count}')
            print(f'Section {section_number}: Durchschnittliche Velocity: {avg_velocity:.3f} m/s')

            self.data_list.append({
                "xs": current_xs,
                "valid_particle_count": valid_particle_count,
                "avg_particle": avg_particle,
                "sd_velocity": sd_velocity,
                "avg_velocity": avg_velocity
            })



            if self.create_pictures:
                if self.limit_Data :
                    reduced_data = plotter.reduce_particles(data, self.limit)
                    plotter(reduced_data, avg_particle, sd_velocity, valid_particle_count, avg_velocity, section_number, left_value,right_value)
                else:
                    # Pass the specific average particle count to the plotter
                    plotter(data, avg_particle, sd_velocity, valid_particle_count, avg_velocity, section_number, left_value,right_value)
        return rows

if __name__ == "__main__":
    file_path = r'D:\Bachelorarbeit\UE5.4\TechnicalFishPass\Saved\Logs\TechnicalFishPass.log'
    main = Main(file_path)
    main()
    #r'D:\Bachelorarbeit\UE5.4\TechnicalFishPass\Saved\Logs\TechnicalFishPass.log'

