import { Link } from 'react-router-dom';
import { Button, Container, Typography } from '@mui/material';

export default function Home() {
  return (
    <Container style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
      <Typography variant="h2" component="div" gutterBottom>
        Classroom Copilot
      </Typography>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <Button variant="contained" component={Link} to="/tldraw" style={{ margin: '10px' }}>
          Go to Tldraw
        </Button>
        <Button variant="contained" component={Link} to="/flow" style={{ margin: '10px' }}>
          Go to Flow
        </Button>
        <Button variant="contained" component={Link} to="/flow-draw" style={{ margin: '10px' }}>
          Go to Flow-Draw
        </Button>
      </div>
    </Container>
  );
}