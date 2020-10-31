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

      <div class="container">
        <Switch>
          <Route path="/rate">
            <Rate />
          </Route>
          <Route path="/">
            <Home />
          </Route>
        </Switch>

        <footer>
          <p>© Fusebox 2020</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
