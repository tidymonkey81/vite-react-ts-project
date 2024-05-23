import { HashRouter, Routes, Route } from 'react-router-dom';
import MenuBar from './pages/components/MenuBar';
import Home from './pages/Home';
import Flow from './pages/Flow';
import Draw from './pages/Draw';
import DrawFile from './pages/DrawFile';
import Slides from './pages/Slides';
import FlowDraw from './pages/FlowDraw';
import NotFound from './pages/NotFound';

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/draw" element={<Draw />} />
      <Route path="/draw-file" element={<DrawFile />} />
      <Route path="/slides" element={<Slides />} />
      <Route path="/flow" element={<Flow />} />
      <Route path="/flow-draw" element={<FlowDraw />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export function WrappedApp() {
  return (
    <HashRouter>
      <div>
        <MenuBar />
      </div>
      <div>
        <App />
      </div>
    </HashRouter>
  );
}