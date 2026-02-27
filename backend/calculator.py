"""
Core pricing calculator logic.
Replicates the Excel formulas from the "Реестр 1 оч" sheet.
"""

try:
    from backend.coefficients import (
        BASE_PRICES, FLOOR_COEFFICIENTS, SIZE_COEFFICIENTS,
        LAYOUT_COEFFICIENTS, GEOMETRY_COEFFICIENTS, ELEVATOR_COEFFICIENTS,
        VIEW_COEFFICIENTS, POSITION_COEFFICIENTS, UNITS_ON_FLOOR_COEFFICIENTS,
        BUILDING_COEFFICIENTS, STORAGE_PRICE_PER_SQM, STORAGE_DISCOUNT,
        PARKING_PRICES, PARKING_DISCOUNT, MAX_APARTMENT_DISCOUNT, BOOKING_FEE,
    )
except ImportError:
    from coefficients import (
        BASE_PRICES, FLOOR_COEFFICIENTS, SIZE_COEFFICIENTS,
        LAYOUT_COEFFICIENTS, GEOMETRY_COEFFICIENTS, ELEVATOR_COEFFICIENTS,
        VIEW_COEFFICIENTS, POSITION_COEFFICIENTS, UNITS_ON_FLOOR_COEFFICIENTS,
        BUILDING_COEFFICIENTS, STORAGE_PRICE_PER_SQM, STORAGE_DISCOUNT,
        PARKING_PRICES, PARKING_DISCOUNT, MAX_APARTMENT_DISCOUNT, BOOKING_FEE,
    )


def calculate_apartment_price(
    apartment_type: str,
    floor: int,
    area_total: float,
    area_summer: float,
    size: str,
    layout: str,
    geometry: str,
    elevator_zone: str,
    view: str,
    position: str,
    units_on_floor: int,
    building: str,
    price_adjustment: float = 0.0,
) -> dict:
    """
    Calculate apartment price based on all parameters.

    Returns a detailed breakdown of all coefficients and final prices.
    """
    # Base price lookup
    base_price = BASE_PRICES.get(apartment_type)
    if base_price is None:
        raise ValueError(f"Unknown apartment type: {apartment_type}")

    # Calculate areas
    area_summer_coeff = round(area_summer * 0.3, 2)
    area_without_summer = round(area_total - area_summer, 2)
    area_with_coeff = round(area_without_summer + area_summer_coeff, 2)

    # Look up all coefficients
    floor_coeff = FLOOR_COEFFICIENTS.get(floor, 0.0)
    size_coeff = SIZE_COEFFICIENTS.get(size, 0.0)
    layout_coeff = LAYOUT_COEFFICIENTS.get(layout, 0.0)
    geometry_coeff = GEOMETRY_COEFFICIENTS.get(geometry, 0.0)
    elevator_coeff = ELEVATOR_COEFFICIENTS.get(elevator_zone, 0.0)
    view_coeff = VIEW_COEFFICIENTS.get(view, 0.0)
    position_coeff = POSITION_COEFFICIENTS.get(position, 0.0)
    units_coeff = UNITS_ON_FLOOR_COEFFICIENTS.get(units_on_floor, 0.0)
    building_coeff = BUILDING_COEFFICIENTS.get(building, 0.0)

    # Sum of all coefficients
    total_coeff = (
        floor_coeff
        + size_coeff
        + layout_coeff
        + geometry_coeff
        + elevator_coeff
        + view_coeff
        + position_coeff
        + units_coeff
        + building_coeff
    )

    # Price per sqm with coefficients (РАСЦЕНКА)
    price_per_sqm = round(base_price + base_price * total_coeff, 2)
    budget = round(price_per_sqm * area_total, 2)

    # Final price with adjustment
    final_price_per_sqm = round(price_per_sqm + price_per_sqm * price_adjustment, 2)
    final_budget = round(final_price_per_sqm * area_total, 2)

    # CRM price (with max discount markup)
    crm_price_per_sqm = round(final_price_per_sqm * (1 + MAX_APARTMENT_DISCOUNT), 2)
    crm_budget = round(crm_price_per_sqm * area_total, 2)

    # Website price (CRM + booking fee)
    site_price_per_sqm = round(crm_price_per_sqm + BOOKING_FEE, 2)
    site_budget = round(site_price_per_sqm * area_total, 2)

    return {
        "input": {
            "apartment_type": apartment_type,
            "floor": floor,
            "area_total": area_total,
            "area_summer": area_summer,
            "size": size,
            "layout": layout,
            "geometry": geometry,
            "elevator_zone": elevator_zone,
            "view": view,
            "position": position,
            "units_on_floor": units_on_floor,
            "building": building,
            "price_adjustment": price_adjustment,
        },
        "areas": {
            "total": area_total,
            "summer": area_summer,
            "summer_with_coeff": area_summer_coeff,
            "without_summer": area_without_summer,
            "with_coeff": area_with_coeff,
        },
        "coefficients": {
            "base_price": base_price,
            "floor": floor_coeff,
            "size": size_coeff,
            "layout": layout_coeff,
            "geometry": geometry_coeff,
            "elevator": elevator_coeff,
            "view": view_coeff,
            "position": position_coeff,
            "units_on_floor": units_coeff,
            "building": building_coeff,
            "total": round(total_coeff, 6),
        },
        "pricing": {
            "price_per_sqm": price_per_sqm,
            "budget": budget,
            "adjustment": price_adjustment,
            "final_price_per_sqm": final_price_per_sqm,
            "final_budget": final_budget,
        },
        "crm": {
            "max_discount": MAX_APARTMENT_DISCOUNT,
            "price_per_sqm": crm_price_per_sqm,
            "budget": crm_budget,
        },
        "site": {
            "booking_fee": BOOKING_FEE,
            "price_per_sqm": site_price_per_sqm,
            "budget": site_budget,
        },
    }


def calculate_storage_price(area: float, with_discount: bool = False) -> dict:
    """Calculate storage room price."""
    price_per_sqm = STORAGE_PRICE_PER_SQM
    if with_discount:
        price_per_sqm = round(price_per_sqm * (1 - STORAGE_DISCOUNT))

    total = round(price_per_sqm * area, 2)

    return {
        "area": area,
        "price_per_sqm": price_per_sqm,
        "discount": STORAGE_DISCOUNT if with_discount else 0,
        "total": total,
    }


def calculate_parking_price(parking_type: str, with_discount: bool = False) -> dict:
    """Calculate parking space price."""
    base_price = PARKING_PRICES.get(parking_type)
    if base_price is None:
        raise ValueError(f"Unknown parking type: {parking_type}")

    price = base_price
    if with_discount:
        price = round(base_price * (1 - PARKING_DISCOUNT))

    return {
        "parking_type": parking_type,
        "base_price": base_price,
        "discount": PARKING_DISCOUNT if with_discount else 0,
        "price": price,
    }
