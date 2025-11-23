// import { useState } from 'react';
// import { Canvas } from '@react-three/fiber';
// import { XR, createXRStore } from '@react-three/xr';
// import Scene from './Scene';
// import Interface from './Interface';
// import { type ModelData } from './types';

// // Use standard 'local' space for VR
// const store = createXRStore({
//   features: ['local'],
//   controller: false
// });

// export default function App() {
//   const [models, setModels] = useState<ModelData[]>([]);

//   return (
//     <div style={{ width: '100vw', height: '100vh', background: '#000' }}>
//       <Interface store={store} setModels={setModels} />

//       <Canvas
//         // 1. Enable Alpha in the WebGL Context
//         gl={{ alpha: true }}

//         // 2. FORCE the renderer to clear to transparent (0 alpha)
//         onCreated={({ gl, scene }) => {
//           gl.setClearColor(0x000000, 0); // r, g, b, alpha (0 = transparent)
//           scene.background = null;       // Ensure no background color object exists
//         }}
//       >
//         <XR store={store}>
//           <ambientLight intensity={0.5} />
//           <directionalLight position={[10, 10, 5]} intensity={1.5} />

//           <Scene models={models} />
//         </XR>
//       </Canvas>
//     </div>
//   );
// }


import Interface from './Interface';

export default function App() {
  return (
    <div style={{ width: '100vw', height: '100vh', background: '#111' }}>
      {/* Just show the UI. The OS handles the 3D part now. */}
      <Interface />
    </div>
  );
}