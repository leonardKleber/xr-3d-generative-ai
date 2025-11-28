import logo from "./assets/react.svg";

export default function SpinningLogo() {
    return (
        <div
            style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                padding: "12px"
            }}
        >
            <img
                src={logo}
                alt="React logo"
                style={{
                    width: "100px",
                    height: "100px",
                    animation: "spin 2s linear infinite"
                }}
            />
            <style>
                {`
                    @keyframes spin {
                        from { transform: rotate(0deg); }
                        to { transform: rotate(360deg); }
                    }
                `}
            </style>
        </div>
    );
}
