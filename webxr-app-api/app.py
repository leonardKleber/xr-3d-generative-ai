# server.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import asyncio
import mimetypes

# Ensure .usdz and .glb are served with the correct MIME type
mimetypes.add_type("model/vnd.usdz+zip", ".usdz")
mimetypes.add_type("model/gltf-binary", ".glb")

# Import your existing services
from services.agent_service import AgentService
from services.image_generation_service import ImageGenerationService
from services.model_3d_service import Model3DService

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Services
agent_service = AgentService()
image_gen_service = ImageGenerationService()
model_3d_service = Model3DService()

# Serve static files (generated models/images)
# Ensure these directories exist
os.makedirs("assets/models", exist_ok=True)
# app.mount("/models", StaticFiles(directory="assets/models"), name="models")


@app.get("/models/{filename}")
async def get_model(filename: str):
    print(f"Serving model: {filename}")
    file_path = os.path.join("assets/models", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Model not found")
    
    # Determine media type based on extension
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

class GenerateRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_3d(request: GenerateRequest):
    print(f"Received Prompt: {request.prompt}")
    
    # 1. Use AgentService to plan/refine prompt (Optional)
    # refined_prompt = agent_service.chat(request.prompt)

    # 2. Generate 2D Image (SANA)
    # Note: You'll need to adapt generate_image_from_prompt to return the path directly
    success, msg, image_path = image_gen_service.generate_image_from_prompt(
        object_name="requested_object", 
        prompt=request.prompt, 
        output_dir="assets/images"
    )
    
    if not success:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {msg}")

    # 3. Generate 3D Model (Trellis)
    success, msg, glb_path = model_3d_service.generate_3d_model(
        image_path=image_path,
        output_dir="assets/models"
    )

    if not success:
        raise HTTPException(status_code=500, detail=f"3D generation failed: {msg}")

    # Return the URL to the generated GLB
    # Note: WebXR typically uses GLB/GLTF. USDZ is for Apple QuickLook.
    # If you specifically need USDZ for Vision Pro, you'll need a conversion step here (e.g. using usd-core).
    filename = os.path.basename(glb_path)
    return {
        "status": "success",
        "modelUrl": f"/models/{filename}"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)