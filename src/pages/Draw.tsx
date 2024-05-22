import { Tldraw } from 'tldraw'
import 'tldraw/tldraw.css'

export default function App() {
    return (
        <div style={{ width: '100%', height: '100%', position: 'fixed', top: '50px' }}>
            <Tldraw />
        </div>
    )
}