// // server.ts
// import express from 'express';
// import type { Request, Response } from 'express'; // Import types separately using 'import type'

// import cors from 'cors';
// import bodyParser from 'body-parser';
// import axios from 'axios';
// // import fs from 'fs'; // Uncomment if saving base64 files

// const app = express();
// app.use(cors());
// app.use(bodyParser.json());

// // Constants
// const PORT = 3001;
// // const NVIDIA_NIM_URL = 'http://127.0.0.1:8000/v1/3d/generate'; 

// interface GenerateRequest {
//     prompt: string;
// }

// app.post('/generate', async (req: Request, res: Response) => {
//     // Type casting the body
//     const { prompt } = req.body as GenerateRequest;
//     console.log(`Requesting 3D model for: ${prompt}`);

//     try {
//         // 1. Real Integration (Example)
//         /*
//         const nimResponse = await axios.post(NVIDIA_NIM_URL, {
//              prompt: prompt,
//              format: 'glb'
//         });
//         */

//         // 2. Mock Response (Duck)
//         // This URL is a public sample GLB file
//         const mockUrl = 'https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/Duck/glTF-Binary/Duck.glb';

//         res.json({
//             status: 'success',
//             modelUrl: mockUrl
//         });

//     } catch (error) {
//         console.error(error);
//         res.status(500).json({ error: 'Failed to generate model' });
//     }
// });

// app.listen(PORT, () => {
//     console.log(`Proxy server running on http://localhost:${PORT}`);
// });


// server.ts
import express from 'express';
import type { Request, Response } from 'express'; // Import types separately using 'import type'
import bodyParser from 'body-parser';
import path from 'path';
import cors from 'cors';

// import fs from 'fs'; // Uncomment if saving base64 files

import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Use standard import syntax
const app = express();

app.use(cors());
app.use(bodyParser.json());

const PORT = 3001;

// 1. Serve Static Files from the 'public' folder
// This lets the frontend access http://.../models/model.usdz
app.use('/models', express.static(path.join(__dirname, 'public'), {
    setHeaders: (res) => {
        // CRITICAL: Apple requires this specific MIME type for AR
        res.set('Content-Type', 'model/vnd.usdz+zip');
    }
}));

interface GenerateRequest {
    prompt: string;
}

app.post('/generate', async (req: Request, res: Response) => {
    const { prompt } = req.body as GenerateRequest;
    console.log(`Received Prompt: ${prompt}`);

    // FAKE DELAY (to make it feel like AI is thinking)
    await new Promise(resolve => setTimeout(resolve, 2000));

    // MOCK RESPONSE
    // We return a .usdz file because that is what Vision Pro needs for "Quick Look"
    res.json({
        status: 'success',
        modelUrl: '/models/robot.usdz'
    });
});

app.listen(PORT, () => {
    console.log(`Proxy server running on http://localhost:${PORT}`);
});