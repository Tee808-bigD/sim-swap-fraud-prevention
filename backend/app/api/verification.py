from fastapi import APIRouter, Depends
from ..services.camara import camara_service

router = APIRouter()

@router.get("/sim-status/{phone_number}")
async def check_sim_status(phone_number: str):
    swap_detected, swap_date = await camara_service.check_sim_swap(phone_number)
    return {
        "phone_number": phone_number,
        "sim_swap_detected": swap_detected,
        "swap_date": swap_date
    }

@router.get("/device-status/{phone_number}")
async def check_device_status(phone_number: str):
    swap_detected, swap_date = await camara_service.check_device_swap(phone_number)
    return {
        "phone_number": phone_number,
        "device_swap_detected": swap_detected,
        "swap_date": swap_date
    }