import { Link } from 'react-router-dom';
import { Button, Container, Typography } from '@mui/material';

export default function Home() {
  return (
    <Container style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
      <Typography variant="h2" component="div" gutterBottom>
        Classroom Copilot
      </Typography>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <Button variant="contained" component={Link} to="/cc-admin" style={{ margin: '10px' }}>
          CC Admin
        </Button>
        <Button variant="contained" component={Link} to="/school-admin" style={{ margin: '10px' }}>
          School Admin
        </Button>
        <Button variant="contained" component={Link} to="/cc" style={{ margin: '10px' }}>
          CC
        </Button>
        <Button variant="contained" component={Link} to="/propagator" style={{ margin: '10px' }}>
          Propagator
        </Button>
        <Button variant="contained" component={Link} to="/draw" style={{ margin: '10px' }}>
          Tldraw
        </Button>
        <Button variant="contained" component={Link} to="/flow" style={{ margin: '10px' }}>
          Flow
        </Button>
        <Button variant="contained" component={Link} to="/flow-draw" style={{ margin: '10px' }}>
          Flow/Draw
        </Button>
      </div>
    </Container>
  );
}