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
    abs_input = os.path.abspath(glb_path)
    output_path = abs_input.replace(".glb", ".usdz")

    if os.path.exists(output_path):
        return output_path

    input_dir = os.path.dirname(abs_input)
    input_filename = os.path.basename(abs_input)
    output_filename = os.path.basename(output_path)

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{input_dir}:/data",
        "plattar/xrutils",
        "usd_from_gltf",
        f"/data/{input_filename}",
        f"/data/{output_filename}"
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error converting GLB to USDZ: {e.stderr.decode('utf-8', errors='ignore')}"
        )

    if not os.path.exists(output_path):
        raise HTTPException(status_code=500, detail="USDZ conversion failed")

    return output_path


@app.get("/models/{filename}")
async def get_model(filename: str):
    file_path = os.path.join("assets/models", filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Model not found")

    if filename.endswith(".glb"):
        usdz_path = convert_glb_to_usdz(file_path)
        return FileResponse(
            path=usdz_path,
            media_type="model/vnd.usdz+zip",
            content_disposition_type="inline",
        )

    if filename.endswith(".usdz"):
        return FileResponse(
            path=file_path,
            media_type="model/vnd.usdz+zip",
            content_disposition_type="inline",
        )

    return FileResponse(
        path=file_path,
        media_type="application/octet-stream",
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
    
    return os.path.basename(glb_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
