from fastapi import FastAPI
from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
import uuid

app = FastAPI()


 #Mini API en FastAPI.

class Medicamento(BaseModel):
    product_id: int
    lot_id: str
    quantity: int

@app.post("/procesar/")
def procesar_medicamento(medicamento: Medicamento):
    
    try:
        if medicamento:
            id = str(uuid.uuid4())
            fecha_procesamiento = datetime.utcnow().isoformat()

            return {
                "processing_id": id,
                "processing_date": fecha_procesamiento,
                "status": "procesado"
            }
        else:
             return JSONResponse(content="Sin datos", status_code=status.HTTP_204_NO_CONTENT)
        
    except Exception as e:
        print(f"Error general: {e}")
        return JSONResponse(
            content={"error": "Error en el servidor", "details": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
@app.get("/estado/{processing_id}")
def obtener_estado(processing_id: str):
    try:
        if processing_id:

            return {
            "processing_id": processing_id,
            "status": "procesado",
            "message": "El Medicamento fue procesado correctamente"
        }
        else:
            return JSONResponse(content="Sin datos", status_code=status.HTTP_204_NO_CONTENT)
        
    except Exception as e:
        print(f"Error general: {e}")
        return JSONResponse(
            content={"error": "Error en el servidor", "details": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    












