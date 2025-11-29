import { BrowserRouter, Routes, Route } from "react-router-dom";
import StartPage from "./pages/StartPage";
import GenerationPage from "./pages/GenerationPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<StartPage />} />
        <Route path="/xr" element={<GenerationPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;