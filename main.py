import tkinter as tk
from tkinter import messagebox
import math


def show_selected_options():
    # Eingabefelder auslesen
    input1 = entry1.get()
    input2 = entry2.get()

    # Ausgewaehlte Optionen auslesen
    selected_options = []
    if option1_var.get():
        selected_options.append("Option 1")
    if option2_var.get():
        selected_options.append("Option 2")
    if option3_var.get():
        selected_options.append("Option 3")

    # Ergebnis anzeigen
    messagebox.showinfo("Selected Options",
                        f"Eingabefeld 1: {input1}\nEingabefeld 2: {input2}\nAusgewählt: {', '.join(selected_options)}")


def calculate():
    try:
        # Wert aus Eingabefeld 1 auslesen und in eine Zahl umwandeln
        HQ100 = (option1_var.get())
        MQ = (option2_var.get())
        Q30 = (option3_var.get())
        XS1BoolBox = (option4_var.get())
        XS2BoolBox = (option5_var.get())
        XS3BoolBox = (option6_var.get())
        XS4BoolBox = (option7_var.get())

        if XS1BoolBox:
            waterleveluser = float(entry1.get())
            velocityuser = float(entry2.get())
        elif XS4BoolBox:
            waterleveluser = float(entry3.get())
            velocityuser = float(entry4.get())
        # else:
        # Fehlermeldung anzeigen, falls die Eingabe keine gültige Zahl ist
        # messagebox.showerror("Fehler", "Füllen Sie bitte alle Eingabfelder aus")

        # XS1 Messpunkt Berechnung: Insgesamt 7 Querschnittsteile
        XS1QS1 = waterleveluser * 40
        XS1QS2 = ((waterleveluser - 20) * 107.5) - ((4.5 * 87.5) / 2)

        # Bedingung: Dreieck abziehen (4,5cm) auf 87,5cm länge zusätzlich keine Werte, wenn Wasserstand kleiner gleich 20cm
        if waterleveluser <= 20:
            XS1QS2 = 0
        elif waterleveluser <= 24.5:
            # 2,944 Grad in Radiant umrechnen
            angle1 = math.radians(2.944)
            # Tangens von 2,944 Grad berechnen und die Länge des Dreickes bestimmen
            length1 = (waterleveluser - 20) / math.tan(angle1)
            XS1QS2 = ((waterleveluser - 20) * 107.5) - (((waterleveluser - 20) * length1) / 2)

        XS1QS3 = ((waterleveluser - 24.5) ** 2) / 2
        if waterleveluser <= 24.5:
            XS1QS3 = 0
        elif waterleveluser >= 50:
            XS1QS3 = 325.125

        XS1QS4 = (waterleveluser ** 2) / 2
        if waterleveluser >= 20:
            XS1QS4 = 200

        # 50 Grad geneigte Wand links am Querschnitt XS1
        angle2 = math.radians(77)
        XS1QS5 = ((waterleveluser ** 2) * math.tan(angle2)) / 2

        XS1QS6 = (((waterleveluser - 50) ** 2) * math.tan(angle2)) / 2
        if waterleveluser <= 50:
            XS1QS6 = 0

        XS1QS7 = ((waterleveluser - 50) * 62.5)
        if waterleveluser <= 50:
            XS1QS7 = 0

        SUMXS1QS = XS1QS1 + XS1QS2 + XS1QS3 + XS1QS4 + XS1QS5 + XS1QS6 + XS1QS7

        # XS4 Messpunkt Berechnung: Insgesamt 7 Querschnittsteile

        if waterleveluser <= 22.5:
            print("Groundfloor")
            XS4QS1 = 0.
            XS4QS2 = waterleveluser * (40 + 2 * waterleveluser)
            XS4QS3 = 0.
            XS4QS4 = 0.
            XS4QS5 = 0.
        if (waterleveluser > 22.5) & (waterleveluser <= 65):
            print("First floor")
            XS4QS1 = (waterleveluser - 22.5) * 5.
            XS4QS2 = 22.5 * (40 + 2 * 22.5)
            XS4QS3 = (waterleveluser - 22.5) * (40 + 2 * 2 * waterleveluser)
            XS4QS4 = 0.5 * (waterleveluser - 22.5) * (130 - 22.5 * 2)
            XS4QS5 = 0.
        if waterleveluser > 65:
            print("Second floor")
            XS4QS1 = (waterleveluser - 22.5) * 5.
            XS4QS2 = 22.5 * (40 + 2 * 22.5)
            XS4QS3 = (65 - 22.5) * (40 + 2 * 2 * 65)
            XS4QS4 = 0.5 * (65 - 22.5) * (130 - 22.5 * 2)
            XS4QS5 = (250 - 5) * (waterleveluser - 65)

        sumXS4QS = XS4QS1 + XS4QS2 + XS4QS3 + XS4QS4 + XS4QS5


        if (XS1BoolBox == True and XS2BoolBox == False and XS3BoolBox == False and XS4BoolBox == False):
            SUM = SUMXS1QS
        elif (XS4BoolBox == True and XS1BoolBox == False and XS2BoolBox == False and XS3BoolBox == False):
            SUM = sumXS4QS
        elif (XS1BoolBox == True and XS4BoolBox == True):
            # Fehlermeldung anzeigen, falls die Eingabe keine gültige Zahl ist
            messagebox.showerror("Fehler", "Bitte wählen Sie nur EINEN Messpunkt")
        else:
            # Fehlermeldung anzeigen, falls die Eingabe keine gültige Zahl ist
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Messpunkt")

        if (HQ100 == True and MQ == False and Q30 == False):
            result = 1000000 / SUM
        elif (MQ == True and Q30 == False and HQ100 == False):
            result = 135000 / SUM
        elif (Q30 == True and HQ100 == False and MQ == False):
            result = 60000 / SUM
        else:
            # Fehlermeldung anzeigen, falls die Eingabe keine gültige Zahl ist
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Szenario für die Berechnung aus.")

        # Vergleich mit gemessener Geschwindigkeit
        Abweichung = ((velocityuser - result) / result) * 100
        result = round(result, 2)
        Abweichung = round(Abweichung, 2)
        Empfehlung = "Das Fluid ist zu viskos"
        if (Abweichung >= 0):
            Empfehlung = "Das Fluid ist zu flüssig"
        messagebox.showinfo("Berechnungsergebnis", f"Das Ergebnis der Berechnung ist: {result} cm/s"
                                                   f"\n"
                                                   f"\n{Empfehlung},um {Abweichung} %")
        # messagebox.showinfo("Berechnungsergebnis", f"Die Abweichung der Berechnung ist: {Abweichung}%")

        if XS1BoolBox == True:
            calculate.SpeedValue1 = result
            if (HQ100 == True and MQ == False and Q30 == False):
                calculate.XS1AbflussMenge = (velocityuser * SUMXS1QS) / 1000000
            elif (MQ == True and Q30 == False and HQ100 == False):
                calculate.XS1AbflussMenge = (velocityuser * SUMXS1QS) / 135000
            elif (Q30 == True and HQ100 == False and MQ == False):
                calculate.XS1AbflussMenge = (velocityuser * SUMXS1QS) / 60000

        elif XS4BoolBox == True:
            calculate.SpeedValue2 = result
            if (HQ100 == True and MQ == False and Q30 == False):
                calculate.XS4AbflussMenge = (velocityuser * sumXS4QS) / 1000000
            elif (MQ == True and Q30 == False and HQ100 == False):
                calculate.XS4AbflussMenge = (velocityuser * sumXS4QS) / 135000
            elif (Q30 == True and HQ100 == False and MQ == False):
                calculate.XS4AbflussMenge = (velocityuser * sumXS4QS) / 60000

    except ValueError:
        # Fehlermeldung anzeigen, falls die Eingabe keine gültige Zahl ist
        messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Zahl in Water Level ein.")
    return result


def massebilanz():
    try:
        SpeedValue1 = calculate.SpeedValue1
        SpeedValue2 = calculate.SpeedValue2
        XS1AbflussMenge = calculate.XS1AbflussMenge
        XS4AbflussMenge = calculate.XS4AbflussMenge

        Abweichung = ((XS1AbflussMenge / XS4AbflussMenge) - 1) * 100
        if Abweichung <= 0:
            Abweichung = Abweichung * (-1)
        Abweichung = round(Abweichung, 2)
        XS1AbflussMenge = round(XS1AbflussMenge, 2)
        XS4AbflussMenge = round(XS4AbflussMenge, 2)

        messagebox.showinfo("Berechnungsergebnis",
                            f"XS1 Bilanz : {XS1AbflussMenge} m^3/s\nXS4 Bilanz : {XS4AbflussMenge} m^3/s"
                            f"\nDie Abweichung beider Werte ist {Abweichung} %")

    except AttributeError:
        # Fehlermeldung anzeigen, falls die Eingabe keine gültige Zahl ist
        messagebox.showerror("Fehler", "Bitte berechnen Sie noch XS4 für die Bilanzergebnisse.")


# Hauptfenster erstellen
root = tk.Tk()
root.title("Berechnung der Viskosität")

option4_var = tk.BooleanVar()
option5_var = tk.BooleanVar()  # XS2
option6_var = tk.BooleanVar()  # XS3
option7_var = tk.BooleanVar()

option8_var = tk.BooleanVar()  # UProfilCheckBox
option9_var = tk.BooleanVar()

tk.Checkbutton(root, text="Messpunkt XS1", variable=option4_var).grid(row=0, column=0, columnspan=1, padx=10, pady=10)
# tk.Checkbutton(root, text="Messpunkt XS2", variable=option5_var).grid(row=0, column=1, padx=10, pady=10)
# tk.Checkbutton(root, text="Messpunkt XS3", variable=option6_var).grid(row=0, column=2, padx=10, pady=10)
tk.Checkbutton(root, text="Messpunkt XS4", variable=option7_var).grid(row=0, column=1, columnspan=1, padx=10, pady=10)

# tk.Checkbutton(root, text="Messpunkt UProfil CS1", variable=option8_var).grid(row=0, column=5, columnspan=1, padx=10, pady=10)
# tk.Checkbutton(root, text="Bilanz XS2 und XS3", variable=option9_var).grid(row=5, column=1, columnspan=1, padx=10, pady=10)

# Eingabefelder
tk.Label(root, text="Water Level:").grid(row=1, column=0, columnspan=1, padx=10, pady=10)
entry1 = tk.Entry(root)
entry1.grid(row=1, column=1, columnspan=1, padx=10, pady=10)

tk.Label(root, text="Velocity:").grid(row=2, column=0, columnspan=1, padx=10, pady=10)
entry2 = tk.Entry(root)
entry2.grid(row=2, column=1, columnspan=1, padx=10, pady=10)

tk.Label(root, text="Water Level2:").grid(row=1, column=2, columnspan=1, padx=10, pady=10)
entry3 = tk.Entry(root)
entry3.grid(row=1, column=3, columnspan=1, padx=10, pady=10)

tk.Label(root, text="Velocity2:").grid(row=2, column=2, columnspan=1, padx=10, pady=10)
entry4 = tk.Entry(root)
entry4.grid(row=2, column=3, columnspan=1, padx=10, pady=10)

# tk.Label(root, text="Water Level UProfil:").grid(row=1, column=4, columnspan=1, padx=10, pady=10)
# entry5 = tk.Entry(root)
# entry5.grid(row=1, column=5, columnspan=1, padx=10, pady=10)

# tk.Label(root, text="Velocity UProfil:").grid(row=2, column=4, columnspan=1, padx=10, pady=10)
# entry6 = tk.Entry(root)
# entry6.grid(row=2, column=5, columnspan=1, padx=10, pady=10)

# Auswahlfelder
option1_var = tk.BooleanVar()
option2_var = tk.BooleanVar()
option3_var = tk.BooleanVar()
# option4_var = tk.BooleanVar()

tk.Checkbutton(root, text="HQ100=1m^3/s", variable=option1_var).grid(row=3, column=0, columnspan=1, padx=10, pady=10)
tk.Checkbutton(root, text="MQ=0,135m^3/s", variable=option2_var).grid(row=3, column=1, columnspan=1, padx=10, pady=10)
tk.Checkbutton(root, text="Q30=0,06m^3/s", variable=option3_var).grid(row=3, column=2, columnspan=1, padx=10, pady=10)
# tk.Checkbutton(root, text="QUProfil=1,5m^3/s", variable=option4_var).grid(row=3, column=5, columnspan=1, padx=10, pady=10)

# Button zum Anzeigen der ausgewählten Optionen
tk.Button(root, text="Massebilanz nachweisen", command=massebilanz).grid(row=6, column=0, columnspan=5, pady=20)

# Button zur Berechnung
tk.Button(root, text="Berechnung durchführen", command=calculate).grid(row=4, column=0, columnspan=5, pady=20)

# Hauptschleife starten
root.mainloop()

