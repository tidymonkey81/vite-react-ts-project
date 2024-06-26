import { HashRouter, Routes, Route } from 'react-router-dom';
import MenuBar from './components/MenuBar';
import Home from './pages/Home';
import NotFound from './pages/NotFound';

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export function WrappedApp() {
  return (
    <HashRouter>
      <MenuBar />
      <App />
    </HashRouter>
  );
}