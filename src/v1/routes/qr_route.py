from fastapi import APIRouter, File, UploadFile
from src.controllers.qr_controller import QrController

router = APIRouter()


@router.get("/link")
async def link(website: str):
    return await QrController.Link(website)


@router.get("/email")
async def email(to: str, sub: str, body: str):
    return await QrController.Email(to, sub, body)


@router.get("/text")
async def text(message: str):
    return await QrController.Text(message)


@router.get("/whatsapp")
async def whatsapp(phone: int, message: str):
    return await QrController.Whatsapp(phone, message)


@router.get("/image")
async def image(file: UploadFile = File(...)):
    return await QrController.Image(file)
