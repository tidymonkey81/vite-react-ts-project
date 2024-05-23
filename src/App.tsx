import { HashRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Flow from './pages/Flow';
import Draw from './pages/Draw';
import DrawFile from './pages/DrawFile';
import Slides from './pages/Slides';
import FlowDraw from './pages/FlowDraw';
import CC from './pages/CC';
import NotFound from './pages/NotFound';
import MenuBar from './pages/components/MenuBar';

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/draw" element={<Draw />} />
      <Route path="/draw-file" element={<DrawFile />} />
      <Route path="/slides" element={<Slides />} />
      <Route path="/flow" element={<Flow />} />
      <Route path="/flow-draw" element={<FlowDraw />} />
      <Route path="/cc" element={<CC />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export function WrappedApp() {
  return (
    <HashRouter>
      <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
        <div>
          <MenuBar />
        </div>
        <div style={{ overflowY: 'auto', flexGrow: 1 }}>
          <App />
        </div>
      </div>
    </HashRouter>
  );
}