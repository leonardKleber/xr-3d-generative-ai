// src/types.ts

// Defines the structure of a 3D object in our scene
export interface ModelData {
    id: string;
    url: string;
    position: [number, number, number]; // Tuple for X, Y, Z
}

// API Response structure
export interface GenerationResponse {
    status: string;
    modelUrl: string;
}