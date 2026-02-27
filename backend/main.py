"""
FastAPI backend for the real estate pricing calculator.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import os

try:
    from backend.calculator import (
        calculate_apartment_price,
        calculate_storage_price,
        calculate_parking_price,
    )
    from backend.coefficients import get_all_options
except ImportError:
    from calculator import (
        calculate_apartment_price,
        calculate_storage_price,
        calculate_parking_price,
    )
    from coefficients import get_all_options

app = FastAPI(title="Калькулятор цен ЖК", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ApartmentRequest(BaseModel):
    apartment_type: str = Field(description="Тип квартиры: Ст, 1К, 2К")
    floor: int = Field(ge=1, le=12, description="Этаж (1-12)")
    area_total: float = Field(gt=0, description="Общая площадь, кв.м")
    area_summer: float = Field(ge=0, description="Площадь летних помещений, кв.м")
    size: str = Field(description="Размер: XS, S, M, L, XL")
    layout: str = Field(description="Тип планировки: Линейная, Угловая")
    geometry: str = Field(description="Геометрия: Правильная, Неправильная")
    elevator_zone: str = Field(description="Удалённость от лифта: Зона 1, 2, 3")
    view: str = Field(description="Виды из окон")
    position: str = Field(description="Расположение на этаже")
    units_on_floor: int = Field(ge=1, description="Количество лотов на этаже")
    building: str = Field(description="Корпус: С1, С2, С3-1, С3-2")
    price_adjustment: float = Field(
        default=0.0, description="Повышение/скидка цены, доля"
    )


class StorageRequest(BaseModel):
    area: float = Field(gt=0, description="Площадь кладовой, кв.м")
    with_discount: bool = Field(default=False, description="Применить скидку")


class ParkingRequest(BaseModel):
    parking_type: str = Field(description="Тип парковочного места")
    with_discount: bool = Field(default=False, description="Применить скидку")


@app.get("/api/options")
def get_options():
    """Get all available dropdown options for the calculator."""
    return get_all_options()


@app.post("/api/calculate/apartment")
def calc_apartment(req: ApartmentRequest):
    """Calculate apartment price with all coefficients."""
    try:
        return calculate_apartment_price(**req.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/calculate/storage")
def calc_storage(req: StorageRequest):
    """Calculate storage room price."""
    return calculate_storage_price(**req.model_dump())


@app.post("/api/calculate/parking")
def calc_parking(req: ParkingRequest):
    """Calculate parking space price."""
    try:
        return calculate_parking_price(**req.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# Serve Vue frontend static files in production
static_dir = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.isdir(static_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        file_path = os.path.join(static_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(static_dir, "index.html"))
