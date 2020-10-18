import React from 'react';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import Nav from './Nav';
import Home from './Home';
import Rate from './Rate';
import './App.css';

function App() {
  return (
    <Router>
      <Nav />

      <Switch>
        <Route path="/rate">
          <Rate />
        </Route>
        <Route path="/">
          <Home />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
