def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    if height_m <= 0:
        return 0
    return weight_kg / (height_m ** 2)