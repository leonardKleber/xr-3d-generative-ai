# xr-3d-generative-ai
A research project at TU Berlin focused on finding user-friendly ways to incorporate generative AI into general Extended Reality use cases.

This project is a WebXR application built for the **Apple Vision Pro**. It allows users to generate 3D assets (simulated via Nvidia NIM microservices), preview them in a 3D Canvas, and place them into their real-world environment using **AR Quick Look** or **VR Passthrough**.

## 🚀 Prerequisites

Before you begin, ensure you have the following installed:

1. **Node.js** (v18 or higher)
2. **Ngrok** (Required for HTTPS tunneling to the Vision Pro) -> [Download Ngrok](https://ngrok.com/download)
3. **Apple Vision Pro** (Running visionOS 1.1 or higher recommended)

---

## 🛠 Setting up the project

### Web App
Navigate to the `webxr-app` folder and run the following commands:
```bash
npm install
npm run dev -- --host
```
#### Optional when used with Apple Vision Pro
Apple Vision Pro **requires HTTPS** for WebXR and AR Quick Look. We use Ngrok to expose your local frontend to the internet securely.

```bash
ngrok http 5173
```

### Web App API
Install dependencies**  
In the `webxr-app-api` directory, run:
```bash
pip install -r requirements.txt
```

Start the API server**  
```bash
python3 app.py
```

### Generative Models
...

---

## 🥽 Running on Vision Pro

1. Put on your **Apple Vision Pro**.
2. Open **Safari**.
3. Enter the **HTTPS Ngrok URL** from Terminal 3.
    * *Note: If you see a "Visit Site" warning from Ngrok, click "Visit Site" to continue.*
4. You should see the "Nvidia NIM 3D Generator" interface.

### How to use the App

1. **Type a prompt** (e.g., "A futuristic robot") and click **Generate**.
2. **Wait** for the loading to finish.
3. **AR Quick Look:** Click the **"View in My Space (AR)"** button.
    * The model will "pop out" of the window.
    * Look at your floor or table to place the object.
    * The object persists in your room even if you minimize Safari.

## Acknowledgements
Parts of this project are based on code and models from the following repository, which we modified for our use case:
```
https://github.com/NVIDIA-AI-Blueprints/3d-object-generation
```

