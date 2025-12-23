from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/download", tags=["Скачивание курсовой"])

@router.get("/kursovaya", summary="Скачать курсовую работу в формате Word")
async def download_kursovaya():
    file_path = "static/KSR.docx"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл курсовой работы не найден")
    
    return FileResponse(
        path=file_path,
        filename="Курсовая_работа_FASTAPI_Отель_Бронирование.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )