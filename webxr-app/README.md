# WebXR & Nvidia NIM Generator for Apple Vision Pro

This project is a WebXR application built for the **Apple Vision Pro**. It allows users to generate 3D assets (simulated via Nvidia NIM microservices), preview them in a 3D Canvas, and place them into their real-world environment using **AR Quick Look** or **VR Passthrough**.

## 🏗 Architecture

* **Frontend:** React, TypeScript, Vite, Three.js (React Three Fiber), USDZLoader.
* **Backend:** Node.js, Express (Proxies requests to Nvidia NIM and serves static 3D files).
* **Device:** Apple Vision Pro (Safari).

---

## 🚀 Prerequisites

Before you begin, ensure you have the following installed:

1. **Node.js** (v18 or higher)
2. **Ngrok** (Required for HTTPS tunneling to the Vision Pro) -> [Download Ngrok](https://ngrok.com/download)
3. **Apple Vision Pro** (Running visionOS 1.1 or higher recommended)

---

## 🛠 Installation

1. **Clone the repository** (or navigate to your project folder):

    ```bash
    cd webxr-app
    ```

2. **Install Dependencies:**

    ```bash
    npm install
    ```

---

## 🏃‍♂️ How to Run

You need **three separate terminals** running simultaneously.

### Terminal 1: The Backend Server

This runs the Express server on port 3001. It handles API requests and serves the 3D files.

```bash
npx ts-node server.ts
```

*Output should say: `Proxy server running on http://localhost:3001`*

### Terminal 2: The Frontend

This runs the Vite development server on port 5173.

```bash
npm run dev -- --host
```

*Output should say: `Local: http://localhost:5173`*

### Terminal 3: The Secure Tunnel (Ngrok)

Apple Vision Pro **requires HTTPS** for WebXR and AR Quick Look. We use Ngrok to expose your local frontend to the internet securely.

```bash
ngrok http 5173
```

*Copy the URL that looks like: `https://xxxx-xxxx.ngrok-free.app`*

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

---

## 🧩 Project Structure

* **`server.ts`**: The Backend.
  * Simulates the AI generation (Mock API).
  * Serves the `.usdz` files with the correct MIME type (`model/vnd.usdz+zip`).
* **`src/App.tsx`**: The Frontend entry point.
* **`src/Interface.tsx`**: The main UI logic.
  * Handles the API call to `/generate`.
  * Renders the `<Canvas>` preview using `USDZLoader`.
  * Generates the `<a rel="ar">` link for Vision Pro Quick Look.
* **`vite.config.ts`**:
  * Configures the **Proxy**. It forwards `/generate` and `/models` requests from port 5173 to port 3001 so the Vision Pro can access them via the tunnel.

---

## 🔌 Integrating Real Nvidia NIM

To switch from the "Fake" robot model to real AI generation:

1. Ensure you have a local Nvidia NIM microservice running (usually on port 8000).
2. Open `server.ts`.
3. Uncomment the `axios.post` call to your NIM endpoint.
4. Save the resulting base64/file output to the `public/` folder dynamically.
5. Use a library like `gltf-to-usdz` (if the NIM returns GLB) to convert the file before sending the URL to the frontend.

---

## 🐛 Troubleshooting

* **"Failed to connect to backend":**
  * Ensure Terminal 1 (Server) is running.
  * Check `vite.config.ts` to ensure the proxy target matches the server port (3001).
* **Model is 404 / Not Found:**
  * Check that `public/robot.usdz` actually exists.
  * Ensure `server.ts` is serving the static folder correctly.
* **AR Button doesn't work:**
  * Ensure the link has `rel="ar"`.
  * Ensure there is an `<img>` tag inside the link (even if hidden).
  * Ensure you are using the **HTTPS** Ngrok link, not `http://192.168...`.
