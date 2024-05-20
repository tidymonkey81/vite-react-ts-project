import { HashRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Flow from './pages/Flow';
import NotFound from './pages/NotFound';

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/flow" element={<Flow />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export function WrappedApp() {
  return (
    <HashRouter>
      <App />
    </HashRouter>
  );
}