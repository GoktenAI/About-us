import math

def calculate_rmse(estimated, ground_truth):
    """
    Pozisyon tahminleri ile referans değerler arasındaki RMS (ortalama) hatayı hesaplar.
    Her iki liste de "[{"x":..., "y":..., "z":...}]" biçiminde olmalıdır.
    """
    errors = []
    for est, gt in zip(estimated, ground_truth):
        dx = est["x"] - gt["x"]
        dy = est["y"] - gt["y"]
        dz = est["z"] - gt["z"]
        dist = math.sqrt(dx**2 + dy**2 + dz**2)
        errors.append(dist)

    return round(sum(errors) / len(errors), 4) if errors else 0.0