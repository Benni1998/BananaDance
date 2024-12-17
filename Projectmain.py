import matplotlib.pyplot as plt
import numpy as np
import re
from matplotlib.gridspec import GridSpec
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MultipleLocator


# Funktion, um die Daten aus einer Datei zu extrahieren und nach Abschnitten zu trennen
def extract_sections_from_file(file_path):
    sections = []
    currentSection = []

    with open(file_path, 'r') as file:
        lines = file.readlines()


    for line in lines:
        if "STOP" in line:
            if currentSection:
                sections.append(currentSection)
                currentSection = []
        else:
            currentSection.append(line)

    if currentSection:
       sections.append(currentSection)

    return sections

# Funktion, um die gültigen Partikel und ihre umgerechneten Werte aus einem Abschnitt zu extrahieren
def extract_valid_particles(section):

    validParticles = []

    for line in section:
        if "LogBlueprintUserMessages" in line:
            # Überprüfen, ob die Zeile KEY, VECTOR und VELOCITY enthält
            keyMatch = re.search(r'KEY: \d+', line)
            vectorMatch = re.search(r'VECTOR: X=[-.\d]+ Y=[-.\d]+ Z=[-.\d]+', line)
            velocityMatch = re.search(r'VELOCITY: [-.\d]+', line)
            xsMatch = re.search(r"XS(\d+)", line)

            if xsMatch:
                xs_value = int(xsMatch.group(1))

            # Nur gültige Partikel speichern
            if keyMatch and vectorMatch and velocityMatch:
                yMatch = re.search(r'Y=([-\d.]+)', line)
                zMatch = re.search(r'Z=([-\d.]+)', line)
                velocityValue = round(float(velocityMatch.group(0).split(": ")[1].replace(",", ".")) / 100, 3)  # Velocity in m/s umrechnen und auf 3 Dezimalstellen runden


                if yMatch and zMatch:
                    yValue = float(yMatch.group(1)) / 100  # Y-Wert von cm in m umrechnen
                    zValue = float(zMatch.group(1)) / 100  # Z-Wert von cm in m umrechnen
                    validParticles.append([yValue, zValue, velocityValue, xs_value])

    dataArray = np.array(validParticles)
    return dataArray

# Funktion, um den Durchschnitt der Velocity zu berechnen
def calculate_average_velocity(data):
    if data.size == 0:
        return 0  # Vermeide Division durch 0
    velocity = data[:, 2]
    return round(np.mean(velocity), 3)  # Durchschnitt berechnen und auf 3 Nachkommastellen runden

def calculate_standart_deviation(data):
    if data.size == 0:
        return 0  # Vermeide Division durch 0
    velocity = data[:, 2]
    return round(np.std(velocity), 3)

# Funktion, um durschnittliche Partikelanzahl pro Cross Section zu berechnen
def calculateAverageParticleCount(sections):
    allParticles11 = 0
    allParticles41 = 0
    allParticles21 = 0
    allParticles22 = 0
    allParticles31 = 0
    allParticles32 = 0
    allParticles12 = 0
    allParticles42 = 0

    xs11Count = 0
    xs41Count = 0
    xs21Count  = 0
    xs22Count = 0
    xs31Count  = 0
    xs32Count = 0
    xs12Count = 0
    xs42Count = 0

    for section_number, section in enumerate(sections, start=1):
        data = extract_valid_particles(section)
        valid_particle_count = len(data)
        if valid_particle_count > 0:
            if (data[section_number, 3] == 1 and section_number < 20):      # wähle richtige XS
                allParticles11 += valid_particle_count                      # addiere Partikelzahl pro Crosssection
                xs11Count += 1                                              # zähle Anzahl an Bilder pro Crosssection
                xs11LastSection = section_number                            # speicher letzte SectionNumber für aktuelle XS
            elif (data[section_number, 3] == 4 and section_number < 40):
                allParticles41 += valid_particle_count
                xs41Count += 1
                xs41LastSection = section_number
            elif (data[section_number, 3] == 2 and section_number < 50):
                allParticles21 += valid_particle_count
                xs21Count += 1
                xs21LastSection = section_number
            elif (data[section_number, 3] == 3 and section_number < 60):
                allParticles31 += valid_particle_count
                xs31Count += 1
                xs31LastSection = section_number
            elif (data[section_number, 3] == 1 and section_number >= 20):
                allParticles12 += valid_particle_count
                xs12Count += 1
                xs12LastSection = section_number
            elif (data[section_number, 3] == 4 and section_number >= 40):
                allParticles42 += valid_particle_count
                xs42Count += 1
                xs42LastSection = section_number
            elif (data[section_number, 3] == 2 and section_number >= 50):
                allParticles22 += valid_particle_count
                xs22Count += 1
                xs22LastSection = section_number
            elif (data[section_number, 3] == 3 and section_number >= 60):
                allParticles32 += valid_particle_count
                xs32Count += 1
                xs32LastSection = section_number

    if(xs11Count != 0):
        averageXS11 = round(allParticles11/xs11Count, 1)
    else:
        averageXS11 = 0
        xs11LastSection = 0

    if (xs41Count != 0):
        averageXS41 = round(allParticles41/xs41Count, 1)
    else:
        averageXS41 = 0
        xs41LastSection = 0

    if (xs21Count != 0):
        averageXS21 = round(allParticles21/xs21Count, 1)
    else:
        averageXS21 = 0
        xs21LastSection = 0

    if (xs31Count != 0):
        averageXS31 = round(allParticles31 / xs31Count, 1)
    else:
        averageXS31 = 0
        xs31LastSection = 0

    if (xs12Count != 0):
        averageXS12 = round(allParticles12 / xs12Count, 1)
    else:
        averageXS12 = 0
        xs12LastSection = 0

    if (xs42Count != 0):
        averageXS42 = round(allParticles42 / xs42Count, 1)
    else:
        averageXS42 = 0
        xs42LastSection = 0

    if (xs22Count != 0):
        averageXS22 = round(allParticles22/xs22Count, 1)
    else:
        averageXS22 = 0
        xs22LastSection = 0

    if (xs32Count != 0):
        averageXS32 = round(allParticles32 / xs32Count, 1)
    else:
        averageXS32 = 0
        xs32LastSection = 0




    diff1242 = (averageXS12 - averageXS42)
    if averageXS12 != 0:
        masse1 = round((diff1242 / (averageXS12) * 100),2)

        print(f"MasseAbweichung XS1 und XS4: {masse1}%")

    else:
        print("Keine Daten vorhanden")



    diff2232 = (averageXS22 - averageXS32)
    if averageXS22 != 0:
        masse2 = round((diff2232 / (averageXS22) * 100),2)

        print(f"MasseAbweichung XS2 und XS3: {masse2}%")

    else:
        print("Keine Daten vorhanden")



    print(f"XS1:{averageXS12}")
    print(f"XS4:{averageXS42}")
    print(f"XS2:{averageXS22}")
    print(f"XS3:{averageXS32}")




    averageParticles = [averageXS11, xs11LastSection, averageXS41, xs41LastSection,      # speicher Endwerte + Nummer des letzen XS-Abschnitts als Array um nur einen Wert
                        averageXS21, xs21LastSection, averageXS31, xs31LastSection,          # als return zu ermöglichen
                       averageXS12, xs12LastSection, averageXS42, xs42LastSection,
                        averageXS22, xs22LastSection, averageXS32, xs32LastSection]


    return averageParticles


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
    cmapName = 'custom_rainbow'
    return LinearSegmentedColormap.from_list(cmapName, colors)



# Funktion, um den Plot zu erstellen und zu speichern
def plot_data(data, avgParticles, sdVelocity, validParticleCount, avgVelocity, sectionNumber):

    outputFilename = f'section_plot_{sectionNumber}.png'

    fontSizeTitle = 64
    fontSizeAxis = 30
    radius = 0.3

    Y = data[:, 0]
    Z = data[:, 1]
    velocity = data[:, 2]
    average = 0

    if(avgParticles[1] >= sectionNumber):          #XS 1.1
        average = avgParticles[0]
    elif (avgParticles[3] >= sectionNumber):       #XS 4.1
        average = avgParticles[2]
    elif (avgParticles[5] >= sectionNumber):       #XS 2.1
        average = avgParticles[4]
    elif (avgParticles[7] >= sectionNumber):       #XS 3.1
        average = avgParticles[6]
    elif (avgParticles[9] >= sectionNumber):       #XS 1.2
        average = avgParticles[8]
    elif (avgParticles[11] >= sectionNumber):      #XS 4.2
        average = avgParticles[10]
    elif (avgParticles[13] >= sectionNumber):      #XS 2.2
        average = avgParticles[12]
    elif (avgParticles[15] >= sectionNumber):      #XS 3.2
        average = avgParticles[14]

    fig = plt.figure(figsize=(68.27, 38.4), dpi=100)
    gs = GridSpec(2, 1, height_ratios=[0.1, 0.9])

    # Scatter plot (second row)
    ax_scatter = fig.add_subplot(gs[1])
    cmap = create_custom_cmap()
    scatter = ax_scatter.scatter(Y, Z, c=velocity, cmap=cmap, vmin=0, vmax=2, alpha=1.0, s=np.pi * (radius * 10) ** 2)
    ax_scatter.set_facecolor('white')

    # Achsenbeschriftungen
    ax_scatter.set_xlabel('Y Values (m)', fontsize=fontSizeTitle)  # Y-Wert in Metern
    ax_scatter.set_ylabel('Z Values (m)', fontsize=fontSizeTitle)  # Z-Wert in Metern

    # Achsen und Gitter
    ax_scatter.yaxis.set_major_locator(MultipleLocator(0.005))  # Beschriftung alle 0.005 Meter
    ax_scatter.grid(True, which='both', axis='y', linestyle='--', color='gray', linewidth=0.7)

    # Grenzen der Y-Achse
    ax_scatter.set_ylim(0, 0.4)  # Z-Werte in Meter

    # Colorbar (first row, above the plot)
    ax_colorbar = fig.add_subplot(gs[0])
    cbar = fig.colorbar(scatter, cax=ax_colorbar, orientation='horizontal', pad=0.0)
    cbar.set_label('Velocity (m/s)', fontsize=fontSizeTitle, labelpad=40)  # labelpad adds space above the colorbar
    cbar.ax.xaxis.set_label_position('top')  # Move the label to the top
    cbar.ax.tick_params(labelsize=fontSizeAxis)

    # Achsenbeschriftungen für x und y
    ax_scatter.tick_params(axis='both', labelsize=fontSizeAxis)

    # Titel unterhalb des Bildes setzen
    plt.suptitle(f'Section {sectionNumber} Results \n'
                 f'Anzahl: {validParticleCount}, Durchschnittliche Anzahl: {average},\n'
                 f' Durchschnitt Velocity: {avgVelocity:.3f} m/s, sdVelocity: {sdVelocity:.3f}',
                 fontsize=fontSizeTitle, y=0.01)

    # Speichern des Bildes
    plt.savefig(outputFilename, format='png', bbox_inches='tight')
    plt.close()



#Start "Main"

# Pfad zur .txt Datei (bitte den Pfad anpassen)
file_path = r'D:\Bachelorarbeit\UE5.4\TechnicalFishPass\Saved\Logs\TechnicalFishPass.log'

# Daten extrahieren und pro Abschnitt speichern
sections = extract_sections_from_file(file_path)

#Berechne durchschnittliche Partikelzahl
averageParticles = calculateAverageParticleCount(sections)


#Erstellen der Bilder pro Sektion
for sectionNumber, section in enumerate(sections, start=1):
    data = extract_valid_particles(section)
    validParticleCount = len(data)                    # Anzahl der gültigen Partikel
    avgVelocity = calculate_average_velocity(data)     # Durchschnitt der gültigen Velocity berechnen
    sdValue = calculate_standart_deviation(data)


    if validParticleCount > 0:
        # print zur Konsole
        print(f'Section {sectionNumber}: Anzahl der gültigen Partikel: {validParticleCount}')
        print(f'Section {sectionNumber}: Durchschnittliche Velocity: {avgVelocity:.3f} m/s')

        #erstellen der Bilder
        plot_data(data, averageParticles, sdValue, validParticleCount, avgVelocity, sectionNumber)

