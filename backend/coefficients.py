"""
Pricing coefficients extracted from the Excel calculator.
Sheet: "Коэфф для прайса 1 оч"
"""

# Base price per sqm by apartment type
BASE_PRICES = {
    "Ст": 327_000,
    "1К": 313_920,   # 327000 + 327000 * (-0.04)
    "2К": 307_380,   # 327000 + 327000 * (-0.06)
}

# Floor coefficients (cumulative)
FLOOR_COEFFICIENTS = {
    12: 0.215,
    11: 0.16,
    10: 0.12,
    9: 0.085,
    8: 0.055,
    7: 0.03,
    6: 0.015,
    5: 0.005,
    4: 0.0,
    3: -0.005,
    2: -0.015,
    1: -0.045,
}

# Size coefficients
SIZE_COEFFICIENTS = {
    "XS": 0.06,
    "S": 0.04,
    "M": 0.0,
    "L": -0.01,
    "XL": -0.02,
}

# Size ranges table (for reference/validation)
SIZE_RANGES = {
    "Ст": {"S": "<30", "M": "30-34", "L": "35-40", "XL": ">40"},
    "1К": {"XS": "<40", "S": "40-45", "M": "45-50", "L": "50-55", "XL": ">55"},
    "2К": {"XL": ">70"},
}

# Layout type coefficients
LAYOUT_COEFFICIENTS = {
    "Угловая": 0.03,
    "Линейная": 0.0,
}

# Geometry coefficients
GEOMETRY_COEFFICIENTS = {
    "Правильная": 0.03,
    "Неправильная": 0.0,
}

# Distance from elevator coefficients
ELEVATOR_COEFFICIENTS = {
    "Зона 1": 0.005,
    "Зона 2": 0.0,
    "Зона 3": -0.005,
}

# View coefficients
VIEW_COEFFICIENTS = {
    "Море": 0.07,
    "Двор+море": 0.05,
    "Озеро": 0.03,
    "Двор юго-запад": 0.02,
    "Двор+озеро": 0.015,
    "Двор юго-восток": 0.01,
    "Двор юг": 0.0,
    "Двор северо-восток": -0.01,
    "Двор север": -0.015,
    "Въездная зона северо-восток": -0.02,
    "Коммерция": -0.02,
    "Въездная зона север": -0.02,
    "Улица северо-восток": -0.02,
    "Улица север": -0.02,
}

# Floor position coefficients
POSITION_COEFFICIENTS = {
    "Стандарт": 0.0,
    "Около/над входной группой": -0.01,
    "Над входом в коммерцию": -0.02,
    "У входа в лифтовый холл": -0.01,
    "Окна на кровлю": -0.005,
    "Внутренний угол": -0.01,
}

# Number of units on floor coefficients
UNITS_ON_FLOOR_COEFFICIENTS = {
    11: 0.015,
    12: 0.014,
    13: 0.013,
    14: 0.012,
    26: 0.0,
    33: -0.007,
    34: -0.008,
    37: -0.011,
    38: -0.012,
    39: -0.013,
    40: -0.014,
    41: -0.015,
    42: -0.016,
}

# Building coefficients
BUILDING_COEFFICIENTS = {
    "С1": 0.0,
    "С2": 0.12,
    "С3-1": 0.0,
    "С3-2": 0.0,
}

# Storage rooms pricing
STORAGE_PRICE_PER_SQM = 250_000
STORAGE_DISCOUNT = 0.05

# Parking pricing
PARKING_PRICES = {
    "Стандартное место": 1_500_000,
    "VIP место": 1_800_000,
    "Место для МГН М4": 1_700_000,
    "Место для электромобилей": 2_000_000,
    "Расширенное место": 2_000_000,
}
PARKING_DISCOUNT = 0.05

# Maximum apartment discount
MAX_APARTMENT_DISCOUNT = 0.10
BOOKING_FEE = 6_000


def get_all_options():
    """Return all available options for the calculator dropdowns."""
    return {
        "apartment_types": list(BASE_PRICES.keys()),
        "floors": list(range(1, 13)),
        "sizes": list(SIZE_COEFFICIENTS.keys()),
        "size_ranges": SIZE_RANGES,
        "layouts": list(LAYOUT_COEFFICIENTS.keys()),
        "geometries": list(GEOMETRY_COEFFICIENTS.keys()),
        "elevator_zones": list(ELEVATOR_COEFFICIENTS.keys()),
        "views": list(VIEW_COEFFICIENTS.keys()),
        "positions": list(POSITION_COEFFICIENTS.keys()),
        "units_on_floor": list(UNITS_ON_FLOOR_COEFFICIENTS.keys()),
        "buildings": list(BUILDING_COEFFICIENTS.keys()),
        "parking_types": list(PARKING_PRICES.keys()),
    }
