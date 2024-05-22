import { HashRouter, Routes, Route } from 'react-router-dom';
import MenuBar from './components/MenuBar';
import Home from './pages/Home';
import Flow from './pages/Flow';
import Draw from './pages/Draw';
import FlowDraw from './pages/FlowDraw';
import NotFound from './pages/NotFound';

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/tldraw" element={<Draw />} />
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
        <App />
      </div>
    </HashRouter>
  );
}