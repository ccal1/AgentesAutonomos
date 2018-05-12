import numpy as np

def ackleyFunc(cromossom):
    value = 0
    c1 = 20
    c2 = 0.2
    c3 = 2 * np.pi

    cromossomTemp = cromossom
    root_mean_square = np.sqrt((cromossomTemp * cromossomTemp).mean())

    value = -c1 * np.exp(-c2 * root_mean_square)

    cosine_mean = np.cos(cromossomTemp * c3).mean()

    value = value - np.exp(cosine_mean) + c1 + np.exp(1)

    return value
