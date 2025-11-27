import { useRef, useState } from 'react';
import { useFrame, type ThreeEvent } from '@react-three/fiber';
import { Gltf } from '@react-three/drei';
import * as THREE from 'three';
import { type ModelData } from './types';

interface DraggableModelProps {
    url: string;
    initialPos: [number, number, number];
}

interface SceneProps {
    models: ModelData[];
}

function DraggableModel({ url, initialPos }: DraggableModelProps) {
    const ref = useRef<THREE.Group>(null);
    const [dragging, setDragging] = useState<boolean>(false);
    const [tempVec] = useState(new THREE.Vector3());

    useFrame((state) => {
        if (dragging && ref.current) {
            const ray = state.raycaster.ray;
            ray.at(1.5, tempVec);
            ref.current.position.lerp(tempVec, 0.2);
        }
    });

    return (
        <group
            ref={ref}
            position={initialPos}
            onPointerDown={(e: ThreeEvent<PointerEvent>) => {
                e.stopPropagation();
                setDragging(true);
            }}
            onPointerUp={() => setDragging(false)}
            onPointerLeave={() => setDragging(false)}
        >
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