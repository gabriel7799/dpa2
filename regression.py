import matplotlib.pyplot as plt




def linear_regression(timestamps,values):

    y=values

    timestamps_days = [(ts - min(timestamps)).days for ts in timestamps]
    x=timestamps_days

    # Berechnung der Durchschnittswerte
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    # Berechnung der Koeffizienten m und b
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = sum((xi - mean_x) ** 2 for xi in x)

    m = numerator / denominator  # Steigung der Regressionsgeraden
    b = mean_y - m * mean_x  # y-Achsenabschnitt der Regressionsgeraden

    # Vorhersage für einen neuen Datenpunkt x_new
    x_new = 365
    y_pred = m * x_new + b

    plt.scatter(x, y, color='blue', label="Datenpunkte")
    plt.plot(x, [m * xi + b for xi in x], color='red', label="Regressionsgerade")
    plt.scatter(x_new, y_pred, color='green', label="Vorhersage")

    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()

    print(f'm={m}')
    print(f'b={b}')
    print(f'Vorhergesagter Wert nach linearer Regression für den 31. Dezember: {y_pred}')
    return y_pred






