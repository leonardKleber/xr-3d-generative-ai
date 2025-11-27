import { useState } from 'react';
import axios from 'axios';


// const API_BASE_URL =  (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/$/, '');


export default function Interface() {
    const [prompt, setPrompt] = useState<string>("A futuristic looking robot");
    const [loading, setLoading] = useState<boolean>(false);
    const [imageFileName, setImageFileName] = useState<string>("");
    const [modelFileName, setModelFileName] = useState<string>("");

    const handleGenerate = async () => {
        setLoading(true);
        setImageFileName("");
        setModelFileName("");

        try {
            const res = await axios.post(`/generate_image`, { prompt : prompt });
            const generatedImage: string = res.data;
            setImageFileName(generatedImage);

            const res2 = await axios.post(`/generate_model`, { image_path: generatedImage });
            setModelFileName(res2.data);
        } catch (err) {
            console.error("Error generating image/model:", err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={styles.container}>
            <h1>XR 3D Generator</h1>
            <p style={{ color: '#aaa' }}>Generate a model and drag it into your room.</p>
            
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
            
            {(imageFileName !== "" && modelFileName !== "") && (
                <div style={styles.resultBox}>
                    <h3>Model Ready!</h3>
                    <a rel="ar" href={`/models/${modelFileName}`}>
                        {(imageFileName !== "" && modelFileName !== "") && (
                            <img 
                                src={`/images/${imageFileName}`} 
                                alt="Tap to View in AR"
                                style={styles.previewImage}
                            />
                        )}
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
