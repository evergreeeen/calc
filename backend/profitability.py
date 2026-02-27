"""
Profitability calculator — replicates the 'Доходность' sheet from calc.xlsx.

Given a lot number and payment type (full / installment), produces:
 - 15-year price-growth projection
 - 10-year hotel-income projection (from key delivery onward)
 - ROI metrics and payback periods
"""

from __future__ import annotations

import json
import math
import os
from datetime import date
from typing import Any

# ─── lot registry ────────────────────────────────────────────────

_LOTS: list[dict] | None = None


def _load_lots() -> list[dict]:
    global _LOTS
    if _LOTS is None:
        path = os.path.join(os.path.dirname(__file__), "lots_data.json")
        with open(path, encoding="utf-8") as f:
            _LOTS = json.load(f)
    return _LOTS


def get_lot_options() -> dict[str, Any]:
    """Return available buildings and lot numbers for the dropdown."""
    lots = _load_lots()
    buildings: dict[str, list[dict]] = {}
    for lot in lots:
        b = lot["building"]
        if b not in buildings:
            buildings[b] = []
        buildings[b].append(
            {
                "number": lot["number"],
                "code": lot["code"],
                "floor": lot["floor"],
                "area": lot["area"],
                "rooms": lot["rooms"],
                "size": lot["size"],
                "status": lot["status"],
            }
        )
    for b in buildings:
        buildings[b].sort(key=lambda x: x["number"])
    return {"buildings": sorted(buildings.keys()), "lots": buildings}


def find_lot(building: str, number: int) -> dict | None:
    lots = _load_lots()
    for lot in lots:
        if lot["building"] == building and lot["number"] == number:
            return lot
    return None


# ─── constants (from Excel: Коэфф для прайса 1 оч + Доходность) ─

KEY_DELIVERY_DATE = date(2029, 11, 1)
BASE_YEAR = 2025

# Price growth: 15 % per year for first 4 years, then 2 %
PRICE_GROWTH_RATES = [0.15, 0.15, 0.15, 0.15] + [0.02] * 11  # 15 years total

# Occupancy rates starting from the year after key delivery (2030–2039)
OCCUPANCY_RATES = [0.35, 0.44, 0.59, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65]
DAYS_PER_YEAR = 365

MANAGEMENT_EXPENSE_RATIO = 0.50   # 50 % to management company
ADR_INDEXATION = 0.08             # 8 % annual ADR growth

# ADR base accommodation rates by (size, view_crm)
# Derived from 'Коэфф для прайса 1 оч' ADR table
# Rows = apartment size (XS→XL), columns = CRM view
_ADR_ACCOMMODATION: dict[str, dict[str, float]] = {
    "XS": {"ул.Морская": 14400, "Двор": 14832, "Море": 15276.96, "Озеро": 15735.27},
    "S":  {"ул.Морская": 14688, "Двор": 15128.64, "Море": 15582.50, "Озеро": 16049.97},
    "M":  {"ул.Морская": 16891.20, "Двор": 17397.94, "Море": 17919.87, "Озеро": 18457.47},
    "L":  {"ул.Морская": 18242.50, "Двор": 18789.77, "Море": 19353.46, "Озеро": 19934.07},
    "XL": {"ул.Морская": 20066.75, "Двор": 20668.75, "Море": 21288.81, "Озеро": 21927.47},
}

# Additional ADR components (base values, indexed same as accommodation)
_ADR_BREAKFAST_BASE = 3500
_ADR_CHILDREN_BASE = 50
_ADR_COWORKING_BASE = 50


def _get_accommodation_rate(size: str, view_crm: str) -> float:
    """Look up the base nightly accommodation rate."""
    size_rates = _ADR_ACCOMMODATION.get(size, _ADR_ACCOMMODATION["S"])
    return size_rates.get(view_crm, size_rates.get("Двор", 14400))


# ─── profitability calculation ───────────────────────────────────

def calculate_profitability(
    building: str,
    number: int,
    installment: bool = False,
) -> dict[str, Any]:
    """Main profitability calculation matching the Доходность sheet."""
    lot = find_lot(building, number)
    if lot is None:
        raise ValueError(f"Лот {building}-{number} не найден")

    purchase_price = (
        lot["installment_price"] if installment else lot["full_payment_price"]
    )
    if not purchase_price:
        raise ValueError("Нет данных о цене лота")

    # ── price projection (15 years: 2025–2039) ──
    years = list(range(BASE_YEAR, BASE_YEAR + len(PRICE_GROWTH_RATES) + 1))
    prices = [purchase_price]
    for rate in PRICE_GROWTH_RATES:
        prices.append(prices[-1] * (1 + rate))

    # Key delivery year index (2029 → index 4)
    kd_year_idx = KEY_DELIVERY_DATE.year - BASE_YEAR
    price_at_delivery = prices[kd_year_idx]
    growth_to_delivery = (price_at_delivery - purchase_price) / purchase_price
    profit_at_delivery = price_at_delivery - purchase_price

    price_at_2039 = prices[-1]
    profit_at_2039 = price_at_2039 - purchase_price

    # ── hotel income (10 years: 2030–2039) ──
    accommodation_base = _get_accommodation_rate(lot["size"], lot["view_crm"])
    breakfast_base = _ADR_BREAKFAST_BASE
    children_base = _ADR_CHILDREN_BASE
    coworking_base = _ADR_COWORKING_BASE

    hotel_years = []
    cumulative_income = 0
    payback_hotel_year = None
    payback_total_year = None

    for i, occupancy in enumerate(OCCUPANCY_RATES):
        year = KEY_DELIVERY_DATE.year + 1 + i  # 2030, 2031, ...
        factor = (1 + ADR_INDEXATION) ** i

        accommodation = accommodation_base * factor
        breakfast = breakfast_base * factor
        children = children_base * factor
        coworking = coworking_base * factor
        adr_total = accommodation + breakfast + children + coworking

        gross_revenue = adr_total * occupancy * DAYS_PER_YEAR
        gross_accommodation = accommodation * occupancy * DAYS_PER_YEAR
        management_expense = gross_accommodation * MANAGEMENT_EXPENSE_RATIO
        owner_income = gross_accommodation - management_expense
        annual_yield = owner_income / purchase_price

        cumulative_income += owner_income

        # Price growth profit at this year
        price_year_idx = year - BASE_YEAR
        price_growth_profit = prices[price_year_idx] - purchase_price if price_year_idx < len(prices) else profit_at_2039

        if payback_hotel_year is None and cumulative_income >= purchase_price:
            payback_hotel_year = i + 1
        if payback_total_year is None and (cumulative_income + price_growth_profit) >= purchase_price:
            payback_total_year = i + 1

        hotel_years.append({
            "year": year,
            "occupancy": occupancy,
            "adr": round(adr_total, 2),
            "accommodation_rate": round(accommodation, 2),
            "gross_revenue": round(gross_revenue, 2),
            "owner_income": round(owner_income, 2),
            "monthly_income": round(owner_income / 12, 2),
            "annual_yield": round(annual_yield, 4),
            "cumulative_income": round(cumulative_income, 2),
        })

    total_hotel_income = cumulative_income
    avg_annual_hotel_income = total_hotel_income / len(OCCUPANCY_RATES)
    avg_annual_hotel_yield = avg_annual_hotel_income / purchase_price

    total_return = total_hotel_income + profit_at_2039
    avg_annual_total = total_return / len(OCCUPANCY_RATES)
    avg_annual_total_yield = avg_annual_total / purchase_price

    return {
        "lot": {
            "code": lot["code"],
            "building": lot["building"],
            "number": lot["number"],
            "floor": lot["floor"],
            "area": lot["area"],
            "rooms": lot["rooms"],
            "size": lot["size"],
            "view": lot["view"],
            "view_crm": lot["view_crm"],
            "status": lot["status"],
        },
        "payment": {
            "installment": installment,
            "purchase_price": round(purchase_price, 2),
            "site_price_sqm": lot["site_price_sqm"],
            "full_payment_price": round(lot["full_payment_price"], 2),
            "installment_price": round(lot["installment_price"], 2),
        },
        "price_projection": {
            "years": years,
            "prices": [round(p, 2) for p in prices],
            "growth_rates": [0] + PRICE_GROWTH_RATES,
            "key_delivery_date": KEY_DELIVERY_DATE.isoformat(),
            "price_at_delivery": round(price_at_delivery, 2),
            "growth_to_delivery": round(growth_to_delivery, 4),
            "profit_at_delivery": round(profit_at_delivery, 2),
            "price_sqm_at_delivery": round(price_at_delivery / lot["area"], 2),
            "price_at_2039": round(price_at_2039, 2),
            "profit_at_2039": round(profit_at_2039, 2),
        },
        "hotel_income": {
            "years": hotel_years,
            "total_income_10y": round(total_hotel_income, 2),
            "avg_annual_income": round(avg_annual_hotel_income, 2),
            "avg_annual_yield": round(avg_annual_hotel_yield, 4),
        },
        "summary": {
            "total_return_10y": round(total_return, 2),
            "avg_annual_total": round(avg_annual_total, 2),
            "avg_annual_total_yield": round(avg_annual_total_yield, 4),
            "payback_hotel_years": payback_hotel_year,
            "payback_total_years": payback_total_year,
        },
    }
