def get_direction_string(angle_degrees):
    angle = (angle_degrees + 360) % 360

    if 337.5 <= angle or angle < 22.5:
        return "Osten"
    elif 22.5 <= angle < 67.5:
        return "Südosten"
    elif 67.5 <= angle < 112.5:
        return "Süden"
    elif 112.5 <= angle < 157.5:
        return "Südwesten"
    elif 157.5 <= angle < 202.5:
        return "Westen"
    elif 202.5 <= angle < 247.5:
        return "Nordwesten"
    elif 247.5 <= angle < 292.5:
        return "Norden"
    elif 292.5 <= angle < 337.5:
        return "Nordosten"
    else:
        return "Unbekannt" # Sollte bei normalen Winkeln nicht vorkommen