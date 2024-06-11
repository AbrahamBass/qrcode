from fastapi import APIRouter
from src.controllers.qr_controller import QrController

router = APIRouter()


@router.get("/link")
async def link(website: str):
    return await QrController.Link(website)


@router.get("/email")
async def email():
    return await QrController.Email()
