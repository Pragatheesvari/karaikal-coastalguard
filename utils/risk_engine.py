def level_to_score(level):

    scores = {
        "Low": 25,
        "Medium": 50,
        "High": 75,
        "Severe": 100
    }

    return scores.get(level, 0)


def calculate_land_risk(
    rainfall,
    drainage_vulnerability,
    agricultural_vulnerability
):

    if rainfall >= 50:
        rainfall_score = 100
    elif rainfall >= 25:
        rainfall_score = 75
    elif rainfall >= 10:
        rainfall_score = 50
    else:
        rainfall_score = 25

    drainage_score = level_to_score(
        drainage_vulnerability
    )

    agriculture_score = level_to_score(
        agricultural_vulnerability
    )

    land_risk = (
        rainfall_score * 0.40
        + drainage_score * 0.30
        + agriculture_score * 0.30
    )

    return round(land_risk)


def calculate_marine_risk(
    wind_speed,
    wave_height,
    sea_level,
    fishing_vulnerability
):

    if wind_speed >= 40:
        wind_score = 100
    elif wind_speed >= 25:
        wind_score = 75
    elif wind_speed >= 15:
        wind_score = 50
    else:
        wind_score = 25

    if wave_height >= 2.5:
        wave_score = 100
    elif wave_height >= 1.5:
        wave_score = 75
    elif wave_height >= 0.75:
        wave_score = 50
    else:
        wave_score = 25

    if sea_level >= 1:
        tide_score = 100
    elif sea_level >= 0.7:
        tide_score = 75
    elif sea_level >= 0.4:
        tide_score = 50
    else:
        tide_score = 25

    fishing_score = level_to_score(
        fishing_vulnerability
    )

    marine_risk = (
        wind_score * 0.25
        + wave_score * 0.35
        + tide_score * 0.15
        + fishing_score * 0.25
    )

    return round(marine_risk)


def calculate_compound_risk(
    land_risk,
    marine_risk
):

    compound = (
        land_risk * 0.55
        + marine_risk * 0.45
    )

    return round(compound)


def get_risk_level(score):

    if score <= 25:
        return "LOW"

    elif score <= 50:
        return "MODERATE"

    elif score <= 75:
        return "HIGH"

    else:
        return "SEVERE"