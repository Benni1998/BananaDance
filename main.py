import matplotlib.pyplot as plt
import numpy as np
import re
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MultipleLocator

# Funktion, um die Daten aus einer Datei zu extrahieren und nach Abschnitten zu trennen
def extract_sections_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    sections = []
    current_section = []

    for line in lines:
        if "STOP" in line:
            if current_section:
                sections.append(current_section)
                current_section = []
        else:
            current_section.append(line)

    if current_section:
        sections.append(current_section)

    return sections

# Funktion, um die gültigen Partikel und ihre umgerechneten Werte aus einem Abschnitt zu extrahieren
def extract_valid_particles(section):
    valid_particles = []

    for line in section:
        if "LogBlueprintUserMessages" in line:
            # Überprüfen, ob die Zeile KEY, VECTOR und VELOCITY enthält
            key_match = re.search(r'KEY: \d+', line)
            vector_match = re.search(r'VECTOR: X=[-.\d]+ Y=[-.\d]+ Z=[-.\d]+', line)
            velocity_match = re.search(r'VELOCITY: [-.\d]+', line)

            # Nur gültige Partikel speichern
            if key_match and vector_match and velocity_match:
                y_match = re.search(r'Y=([-\d.]+)', line)
                z_match = re.search(r'Z=([-\d.]+)', line)
                velocity_value = round(float(velocity_match.group(0).split(": ")[1].replace(",", ".")) / 100, 2)  # Velocity in m/s umrechnen und auf 2 Dezimalstellen runden


                if y_match and z_match:
                    y_value = float(y_match.group(1)) / 100  # Y-Wert von cm in m umrechnen
                    z_value = float(z_match.group(1)) / 100  # Z-Wert von cm in m umrechnen
                    valid_particles.append([y_value, z_value, velocity_value])

    data_array = np.array(valid_particles)
    return data_array

# Funktion, um den Durchschnitt der Velocity zu berechnen
def calculate_average_velocity(data):
    if data.size == 0:
        return 0  # Vermeide Division durch 0
    velocity = data[:, 2]
    return round(np.mean(velocity), 2)  # Durchschnitt berechnen und auf 2 Nachkommastellen runden

# Benutzerdefinierte Colormap erstellen
def create_custom_cmap():
    colors = [
        (0.0, (0, 0, 0.5)),  # Dunkelblau bei Wert 0
        (0.125, (0, 0, 1.0)),  # Blau bei Wert 0.25 m/s
        (0.375, (0, 1.0, 1.0)),  # Cyan bei Wert 0.75 m/s
        (0.5, (0, 1.0, 0)),  # Grün bei Wert 1 m/s
        (0.625, (1.0, 1.0, 0)),  # Gelb bei Wert 1.25 m/s
        (0.875, (1.0, 0, 0)),  # Rot bei Wert 1.75 m/s
        (1.0, (0.5, 0, 0))  # Dunkelrot bei Wert 2.00 m/s
    ]
    cmap_name = 'custom_rainbow'
    return LinearSegmentedColormap.from_list(cmap_name, colors)

# Funktion, um den Plot zu erstellen und zu speichern
def plot_data(data, output_filename, valid_particle_count, avg_velocity, section_number, radius=0.05, font_size=40):
    Y = data[:, 0]
    Z = data[:, 1]
    velocity = data[:, 2]

    plt.figure(figsize=(38.4, 21.6), dpi=100)
    cmap = create_custom_cmap()
    scatter = plt.scatter(Y, Z, c=velocity, cmap=cmap, vmin=0, vmax=2, alpha=1.0, s=np.pi * (radius * 10) ** 2)

    plt.gca().set_facecolor('white')

    plt.xlabel('Y Values (m)', fontsize=font_size)  # Y-Wert jetzt in Meter
    plt.ylabel('Z Values (m)', fontsize=font_size)  # Z-Wert jetzt in Meter
    plt.title(f'Section {section_number} Results (Anzahl: {valid_particle_count}, Durchschnitt Velocity: {avg_velocity:.2f} m/s)', fontsize=font_size + 4)

    plt.gca().yaxis.set_major_locator(MultipleLocator(0.02))  # Achsenbeschriftung in Metern
    plt.grid(True, which='both', axis='y', linestyle='--', color='gray', linewidth=0.7)

    #plt.xlim(-2.54, 0.91)  # Werte auf Meter angepasst
    plt.ylim(-0.01, 0.5)  # Werte auf Meter angepasst

    cbar = plt.colorbar(scatter, ticks=np.arange(0, 2.1, 0.2), orientation='horizontal')  # Farblegende für Velocity in m/s
    cbar.set_label('Velocity (m/s)', fontsize=font_size)
    cbar.ax.tick_params(labelsize=font_size)

    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)

    plt.savefig(output_filename, format='png', bbox_inches='tight')
    plt.close()

# Pfad zur .txt Datei (bitte den Pfad anpassen)
file_path = r'D:\Bachelorarbeit\UE5.4\TechnicalFishPass\Saved\Logs\TechnicalFishPass.log'

# Daten extrahieren und pro Abschnitt plotten
sections = extract_sections_from_file(file_path)

for section_number, section in enumerate(sections, start=1):
    data = extract_valid_particles(section)
    valid_particle_count = len(data)  # Anzahl der gültigen Partikel
    avg_velocity = calculate_average_velocity(data)  # Durchschnitt der gültigen Velocity berechnen

    if valid_particle_count > 0:
        print(f'Section {section_number}: Anzahl der gültigen Partikel: {valid_particle_count}')
        print(f'Section {section_number}: Durchschnittliche Velocity: {avg_velocity:.2f} m/s')
        output_filename = f'section_plot_{section_number}.png'
        plot_data(data, output_filename, valid_particle_count, avg_velocity, section_number, font_size=30)
