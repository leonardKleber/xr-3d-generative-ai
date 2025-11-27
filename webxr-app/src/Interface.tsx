import { useState } from 'react';
import axios from 'axios';

export default function Interface() {
    const [prompt, setPrompt] = useState<string>("A futuristic looking robot");
    const [loading, setLoading] = useState<boolean>(false);
    
    const [imageFileName1, setImageFileName1] = useState<string>("");
    const [imageFileName2, setImageFileName2] = useState<string>("");
    const [imageFileName3, setImageFileName3] = useState<string>("");
    const [imageFileName4, setImageFileName4] = useState<string>("");

    const [finalImageName, setFinalImageName] = useState<string>("");

    const [modelFileName, setModelFileName] = useState<string>("");

    const [renderImageView, setRenderImageView] = useState<boolean>(false);
    const [renderFinalImage, setRenderFinalImage] = useState<boolean>(false);

    const handleImageSelect = async (number: number) => {
        let selected: string = "";

        if (number === 1) {
            selected = imageFileName1;
        } else if (number === 2) {
            selected = imageFileName2;
        } else if (number === 3) {
            selected = imageFileName3;
        } else if (number === 4) {
            selected = imageFileName4;
        }

        setFinalImageName(selected);

        try {
            const res = await axios.post(`/generate_model`, { image_path: selected });
            setModelFileName(res.data);
        } catch (err) {
            console.error("Error generating model:", err);
        } finally {
            setRenderFinalImage(true);
        }
    };

    const handleInitialGenerate = async () => {
        setLoading(true);
        setImageFileName1("");
        setImageFileName2("");
        setImageFileName3("");
        setImageFileName4("");

        try {
            const res1 = await axios.post(`/generate_image`, { prompt : prompt });
            setImageFileName1(res1.data);

            const res2 = await axios.post(`/generate_image`, { prompt : prompt });
            setImageFileName2(res2.data);

            const res3 = await axios.post(`/generate_image`, { prompt : prompt });
            setImageFileName3(res3.data);

            const res4 = await axios.post(`/generate_image`, { prompt : prompt });
            setImageFileName4(res4.data);
        } catch (err) {
            console.error("Error generating image:", err);
        } finally {
            setLoading(false);
            setRenderImageView(true);
        }
    };

    return (
        <div style={styles.container}>
            <h1>XR 3D Generator</h1>
            <p style={{ color: '#aaa' }}>Generate a model and drag it into your room.</p>
            
            {renderImageView ? (
                <div>
                    {renderFinalImage ? (
                        <div style={styles.resultBox}>
                            <h3>Model Ready!</h3>
                            <a rel="ar" href={`/models/${modelFileName}`}>
                                <img 
                                    src={`/images/${finalImageName}`} 
                                    alt="Tap to View in AR"
                                    style={styles.previewImage}
                                />
                            </a>
                            <p style={{ fontSize: '12px' }}>Tap the icon above to place in room</p>
                        </div>
                    ) : (
                        <div style={styles.imageGridContainer}>
                            <img
                                src={`/images/${imageFileName1}`}
                                alt="Image 1"
                                style={styles.gridImage}
                                onClick={() => handleImageSelect(1)}
                            />
                            <img
                                src={`/images/${imageFileName2}`}
                                alt="Image 2"
                                style={styles.gridImage}
                                onClick={() => handleImageSelect(2)}
                            />
                            <img
                                src={`/images/${imageFileName3}`}
                                alt="Image 3"
                                style={styles.gridImage}
                                onClick={() => handleImageSelect(3)}
                            />
                            <img
                                src={`/images/${imageFileName4}`}
                                alt="Image 4"
                                style={styles.gridImage}
                                onClick={() => handleImageSelect(4)}
                            />
                        </div>
                    )}
                </div>
            ) : (
                <div style={styles.inputGroup}>
                    <input
                        style={styles.input}
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        placeholder="Describe your object..."
                    />
                    <button style={styles.button} onClick={handleInitialGenerate} disabled={loading}>
                        {loading ? "Generating..." : "Generate"}
                    </button>
                </div>
            )}

            {/* 
            
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

            */}
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
    arButton: { padding: '10px 20px', background: 'white', color: 'black', border: 'none', borderRadius: '20px', fontWeight: 'bold', cursor: 'pointer' },
    imageGridContainer: {
        display: "grid",
        gridTemplateColumns: "repeat(2, 1fr)",
        gap: "10px",
        width: "100%",
        maxWidth: "350px",
        margin: "0 auto",
    },

    gridImage: {
        width: "100%",
        height: "auto",
        borderRadius: "8px",
        objectFit: "cover",
        cursor: "pointer",
    }
};
