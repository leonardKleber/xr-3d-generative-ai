from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import mimetypes
import subprocess

mimetypes.add_type("model/vnd.usdz+zip", ".usdz")
mimetypes.add_type("model/gltf-binary", ".glb")

from services.image_generation_service import ImageGenerationService
from services.model_3d_service import Model3DService


BLENDER_EXE = "blender"   # or full path e.g. "C:/Program Files/Blender/blender.exe"
CONVERTER_SCRIPT = "glb_to_usdz.py"   # path to your Python script


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


def convert_glb_to_usdz(glb_path: str) -> str:
    if not os.path.exists(glb_path):
        raise FileNotFoundError(f"GLB file not found: {glb_path}")

    output_usdz = glb_path.replace(".glb", ".usdz")

    cmd = [
        BLENDER_EXE,
        "--background",
        "--factory-startup",
        "--python", CONVERTER_SCRIPT,
        "--",
        glb_path,
        output_usdz
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return output_usdz

    except subprocess.CalledProcessError as e:
        print("Blender conversion error:", e.stderr.decode())
        raise RuntimeError("USDZ conversion failed")


@app.get("/models/{filename}")
async def get_model(filename: str):
    file_path = os.path.join("assets/models", filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Model not found")

    if filename.endswith(".glb"):
        try:
            file_path = convert_glb_to_usdz(file_path)
            filename = os.path.basename(file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"USDZ conversion error: {e}")

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

    # Convert model from glb to usdz
    

    if not success:
        raise HTTPException(
            status_code=500, 
            detail=f"3D generation failed: {msg}"
        )
    
    return os.path.basename(glb_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
