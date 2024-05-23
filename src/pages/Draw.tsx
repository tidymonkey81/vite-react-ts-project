import { Tldraw } from 'tldraw'
import 'tldraw/tldraw.css'

export default function App() {
    return (
        <div style={{ display: 'flex', height: 'calc(100vh - 75px)' }}>
            <div style={{ flex: 1 }}>
                <Tldraw persistenceKey="draw-persistence-key" />
            </div>
        </div>
    )
}