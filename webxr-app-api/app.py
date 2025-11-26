from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import mimetypes
import re

mimetypes.add_type("model/vnd.usdz+zip", ".usdz")
mimetypes.add_type("model/gltf-binary", ".glb")

from services.image_generation_service import ImageGenerationService
from services.model_3d_service import Model3DService


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
image_gen_service = ImageGenerationService()
model_3d_service = Model3DService()
os.makedirs("assets/models", exist_ok=True)


class GenerateImageRequest(BaseModel):
    prompt: str


class GenerateModelRequest(BaseModel):
    image_path: str


@app.get("/models/{filename}")
async def get_model(filename: str):
    file_path = os.path.join("assets/models", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Model not found")
    
    media_type = "application/octet-stream"
    if filename.endswith(".usdz"):
        media_type = "model/vnd.usdz+zip"
    elif filename.endswith(".glb"):
        media_type = "model/gltf-binary"

    return FileResponse(
        path=file_path, 
        media_type=media_type,
        content_disposition_type="inline"
    )


@app.get("/images/{filename}")
async def get_model(filename: str):
    file_path = os.path.join("assets/images", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(
        path=file_path, 
        content_disposition_type="inline"
    )


@app.post("/generate_image")
async def generate_image(request: GenerateImageRequest):
    success, msg, image_path = image_gen_service.generate_image_from_prompt(
        object_name="requested_object", 
        prompt=request.prompt, 
        output_dir="assets/images"
    )
    if not success:
        raise HTTPException(
            status_code=500, 
            detail=f"Image generation failed: {msg}"
        )
    return os.path.basename(image_path)


@app.post("/generate_model")
async def generate_model(request: GenerateModelRequest):
    success, msg, glb_path = model_3d_service.generate_3d_model(
        image_path=f"assets/images/{request.image_path}",
        output_dir="assets/models"
    )
    if not success:
        raise HTTPException(
            status_code=500, 
            detail=f"3D generation failed: {msg}"
        )
    filename = os.path.basename(glb_path)
    return f"/models/{filename}"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
