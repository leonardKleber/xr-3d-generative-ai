import { useState } from 'react';
import axios from 'axios';
import { type GenerationResponse } from './types';

// We don't need the 'store' or 'setModels' props for this specific feature
// because Quick Look handles the 3D part natively, not inside the Canvas.
interface InterfaceProps {
    store?: any;
    setModels?: any;
}

export default function Interface({ }: InterfaceProps) {
    const [prompt, setPrompt] = useState<string>("A futuristic looking robot");
    const [loading, setLoading] = useState<boolean>(false);

    // Store the generated URL here
    const [generatedFile, setGeneratedFile] = useState<string | null>(null);

    const handleGenerate = async () => {
        setLoading(true);
        setGeneratedFile(null); // Reset previous result

        try {
            // const response = await axios.post<GenerationResponse>('http://localhost:3001/generate', {
            //     prompt: prompt
            // });
            const response = await axios.post<GenerationResponse>('/generate', {
                prompt: prompt
            });

            // Save the USDZ/Reality file URL
            setGeneratedFile(response.data.modelUrl);

        } catch (error) {
            console.error("Generation failed:", error);
            alert("Failed to connect to backend");
        }
        setLoading(false);
    };

    return (
        <div style={styles.container}>
            <h1>XR 3D Generator</h1>
            <p style={{ color: '#aaa' }}>Generate a model and drag it into your room.</p>

            {/* INPUT SECTION */}
            <div style={styles.inputGroup}>
                <input
                    style={styles.input}
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Describe your object..."
                />
                <button style={styles.button} onClick={handleGenerate} disabled={loading}>
                    {loading ? "Generating..." : "Generate"}
                </button>
            </div>

            {/* RESULT SECTION */}
            {generatedFile && (
                <div style={styles.resultBox}>
                    <h3>Model Ready!</h3>

                    {/* 
                        Safari Quick Look Requirements:
                        1. rel="ar"
                        2. href points to .usdz file
                        3. Contains an <img> tag (can be a thumbnail or an icon)
                    */}
                    <a rel="ar" href={generatedFile}>
                        <img
                            // Just a placeholder thumbnail image
                            src="https://developer.apple.com/augmented-reality/quick-look/models/vintagerobot2k/vintagerobot2k.jpg"
                            alt="Tap to View in AR"
                            style={styles.previewImage}
                        />
                    </a>
                    <p style={{ fontSize: '12px' }}>Tap the icon above to place in room</p>
                </div>
            )}
        </div>
    );
}

const styles: { [key: string]: React.CSSProperties } = {
    container: {
        position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
        zIndex: 10, color: 'white', background: '#222', padding: '40px', borderRadius: '20px',
        textAlign: 'center', width: '400px', display: 'flex', flexDirection: 'column', gap: '20px'
    },
    inputGroup: { display: 'flex', gap: '10px' },
    input: { flex: 1, padding: '12px', borderRadius: '8px', border: 'none', fontSize: '16px' },
    button: { padding: '12px 24px', cursor: 'pointer', background: '#00d2ff', border: 'none', borderRadius: '8px', fontWeight: 'bold' },
    resultBox: { marginTop: '20px', padding: '20px', background: '#333', borderRadius: '15px' },
    previewImage: { width: '150px', height: '150px', objectFit: 'cover', borderRadius: '10px', marginBottom: '15px' },
    arButton: { padding: '10px 20px', background: 'white', color: 'black', border: 'none', borderRadius: '20px', fontWeight: 'bold', cursor: 'pointer' }
};
