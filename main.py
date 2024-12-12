import tkinter as tk
from tkinter import messagebox
import math


def show_selected_options():
    # Eingabefelder auslesen
    input1 = entry1.get()
    input2 = entry2.get()

    # Optionen auslesen
    selected_options = []
    if option1_var.get():
        selected_options.append("Option 1")
    if option2_var.get():
        selected_options.append("Option 2")
    if option3_var.get():
        selected_options.append("Option 3")

    # Ergebnis anzeigen
    messagebox.showinfo(
        "Selected Options",
        f"Eingabefeld 1: {input1}\nEingabefeld 2: {input2}\nAusgewählt: {', '.join(selected_options)}"
    )


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

        # XS1 Messpunkt Berechnung: Insgesamt 9 Querschnittsteile:
        # Trapezbodenbreite 43cm nicht 40cm
        XS1QS1 = waterleveluser * 43

        # Winkel der Wand 70Grad also Innenwinkel = 20Grad für tan Berechnung
        angle2 = math.radians(20)
        XS1QS2 = ((waterleveluser ** 2) * math.tan(angle2)) / 2

        # Berechnen der XS Teilquerschnittsflaechen QS
        if waterleveluser <= 20:
            XS1QS3 = (waterleveluser ** 2) * 0.5
            XS1QS4 = XS1QS5 = XS1QS6 = XS1QS7 = XS1QS8 = XS1QS9 = 0.

        if (waterleveluser > 20) & (waterleveluser <= 24.5):
            XS1QS3 = 200
            XS1QS4 = 20 * (waterleveluser - 20)
            XS1QS5 = 87.5 * 0.5 * (waterleveluser - 20)
            XS1QS6 = XS1QS7 = XS1QS8 = XS1QS9 = 0

        if (waterleveluser > 24.5) & (waterleveluser <= 50):
            XS1QS3 = 200
            XS1QS4 = 20 * (waterleveluser - 20)
            XS1QS5 = 87.5 * 0.5 * 4.5
            XS1QS6 = 87.5 * (waterleveluser - 24.5)
            XS1QS7 = 0.5 * ((waterleveluser - 24.5)**2)
            XS1QS8 = XS1QS9 = 0

        if waterleveluser > 50:
            XS1QS3 = 200
            XS1QS4 = 20 * (waterleveluser - 20)
            XS1QS5 = 87.5 * 0.5 * 4.5
            XS1QS6 = 87.5 * (waterleveluser - 24.5)
            XS1QS7 = 0.5 * (25.5**2)
            XS1QS8 = (33.5 + 25.5) * (waterleveluser - 50)

            # selber Winkel 70Grad wie linke Wand daher nochmal 20Grad zur Berechnung
            XS1QS9 = (((waterleveluser - 50) ** 2) * math.tan(angle2)) / 2

        SUMXS1QS = XS1QS1 + XS1QS2 + XS1QS3 + XS1QS4 + XS1QS5 + XS1QS6 + XS1QS7 + XS1QS8 + XS1QS9
        print(SUMXS1QS)

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

        if XS1BoolBox and XS2BoolBox == False and XS3BoolBox == False and XS4BoolBox == False:
            SUM = SUMXS1QS
        elif XS4BoolBox and XS1BoolBox == False and XS2BoolBox == False and XS3BoolBox == False:
            SUM = sumXS4QS
        elif XS1BoolBox and XS4BoolBox:
            # Fehlermeldung anzeigen, falls die Eingabe keine gültige Zahl ist
            messagebox.showerror("Fehler", "Bitte wählen Sie nur EINEN Messpunkt")
        else:
            # Fehlermeldung anzeigen
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Messpunkt")

        if HQ100 and MQ == False and Q30 == False:
            result = 1000000 / SUM
        elif MQ and Q30 == False and HQ100 == False:
            result = 135000 / SUM
        elif Q30 and HQ100 == False and MQ == False:
            result = 60000 / SUM
        else:
            # Fehlermeldung anzeigen
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Szenario für die Berechnung aus.")

        # Vergleich mit gemessener Geschwindigkeit
        Abweichung = (velocityuser - result) / result * 100
        result = round(result, 2)
        Abweichung = round(Abweichung, 2)
        Empfehlung = "Das Fluid ist zu viskos"
        if (Abweichung >= 0):
            Empfehlung = "Das Fluid ist zu flüssig"
        messagebox.showinfo(
            "Berechnungsergebnis",
            f"Das Ergebnis der Berechnung ist: {result} cm/s"
                                                   f"\n"
                                                   f"\n{Empfehlung},um {Abweichung} %"
        )

        if XS1BoolBox:
            calculate.SpeedValue1 = result
            if HQ100 and MQ == False and Q30 == False:
                calculate.XS1AbflussMenge = (velocityuser * SUMXS1QS) / 1000000
            elif MQ and Q30 == False and HQ100 == False:
                calculate.XS1AbflussMenge = (velocityuser * SUMXS1QS) / 135000
            elif Q30  and HQ100 == False and MQ == False:
                calculate.XS1AbflussMenge = (velocityuser * SUMXS1QS) / 60000

        elif XS4BoolBox:
            calculate.SpeedValue2 = result
            if HQ100 and MQ == False and Q30 == False:
                calculate.XS4AbflussMenge = (velocityuser * sumXS4QS) / 1000000
            elif MQ and Q30 == False and HQ100 == False:
                calculate.XS4AbflussMenge = (velocityuser * sumXS4QS) / 135000
            elif Q30 and HQ100 == False and MQ == False:
                calculate.XS4AbflussMenge = (velocityuser * sumXS4QS) / 60000

    except ValueError:
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

        messagebox.showinfo(
            "Berechnungsergebnis",
            f"XS1 Bilanz : {XS1AbflussMenge} m^3/s\nXS4 Bilanz : {XS4AbflussMenge} m^3/s"
                            f"\nDie Abweichung beider Werte ist {Abweichung} %"
        )

    except AttributeError:
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
tk.Checkbutton(root, text="Messpunkt XS4", variable=option7_var).grid(row=0, column=1, columnspan=1, padx=10, pady=10)

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

# Auswahlfelder
option1_var = tk.BooleanVar()
option2_var = tk.BooleanVar()
option3_var = tk.BooleanVar()
# option4_var = tk.BooleanVar()

tk.Checkbutton(root, text="HQ100=1m^3/s", variable=option1_var).grid(row=3, column=0, columnspan=1, padx=10, pady=10)
tk.Checkbutton(root, text="MQ=0,135m^3/s", variable=option2_var).grid(row=3, column=1, columnspan=1, padx=10, pady=10)
tk.Checkbutton(root, text="Q30=0,06m^3/s", variable=option3_var).grid(row=3, column=2, columnspan=1, padx=10, pady=10)

# Button zum Anzeigen der ausgewählten Optionen
tk.Button(root, text="Massebilanz nachweisen", command=massebilanz).grid(row=6, column=0, columnspan=5, pady=20)

# Button zur Berechnung
tk.Button(root, text="Berechnung durchführen", command=calculate).grid(row=4, column=0, columnspan=5, pady=20)

# Hauptschleife starten
root.mainloop()
