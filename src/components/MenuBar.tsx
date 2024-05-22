import React from 'react';
import { Link } from 'react-router-dom';
import { Button, Box } from '@mui/material';

const MenuBar = () => {
  return (
    <Box display="flex" justifyContent="space-around" bgcolor="white">
      <Button variant="contained" component={Link} to="/">
        HOME
      </Button>
      <Button variant="contained" component={Link} to="/tldraw">
        TLDRAW
      </Button>
      <Button variant="contained" component={Link} to="/flow">
        FLOW
      </Button>
      <Button variant="contained" component={Link} to="/flow-draw">
        FLOW-DRAW
      </Button>
    </Box>
  );
};

export default MenuBar;