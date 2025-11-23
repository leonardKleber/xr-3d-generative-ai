import { useRef, useState } from 'react';
import { useFrame, type ThreeEvent } from '@react-three/fiber';
import { Gltf } from '@react-three/drei';
import * as THREE from 'three';
import { type ModelData } from './types';

// Props for the individual draggable object
interface DraggableModelProps {
    url: string;
    initialPos: [number, number, number];
}

function DraggableModel({ url, initialPos }: DraggableModelProps) {
    // Type the Ref as a Three.js Group
    const ref = useRef<THREE.Group>(null);
    const [dragging, setDragging] = useState<boolean>(false);
    const [tempVec] = useState(new THREE.Vector3());

    useFrame((state) => {
        if (dragging && ref.current) {
            // Raycaster logic to follow gaze/pinch
            const ray = state.raycaster.ray;

            // Calculate point 1.5 meters down the ray
            ray.at(1.5, tempVec);

            // Smoothly interpolate position
            ref.current.position.lerp(tempVec, 0.2);
        }
    });

    return (
        <group
            ref={ref}
            position={initialPos}
            // Pointer events work for Mouse (PC) and Gaze+Pinch (Vision Pro)
            onPointerDown={(e: ThreeEvent<PointerEvent>) => {
                e.stopPropagation(); // Prevent clicking through the object
                setDragging(true);
            }}
            onPointerUp={() => setDragging(false)}
            onPointerLeave={() => setDragging(false)}
        >
            {/* Bounding box visualizer when dragging */}
            {dragging && (
                <mesh>
                    <boxGeometry args={[0.6, 0.6, 0.6]} />
                    <meshBasicMaterial wireframe color="yellow" />
                </mesh>
            )}

            <Gltf src={url} scale={0.5} />
        </group>
    );
}

interface SceneProps {
    models: ModelData[];
}

export default function Scene({ models }: SceneProps) {
    return (
        <>
            {models.map((model) => (
                <DraggableModel
                    key={model.id}
                    url={model.url}
                    initialPos={model.position}
                />
            ))}
        </>
    );
}