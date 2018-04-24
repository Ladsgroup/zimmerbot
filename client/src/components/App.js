import React, { Component } from 'react';
import Home from './Home';
import Header from './Header';
import { BrowserRouter, Route } from 'react-router-dom';
import '../styles/index.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <BrowserRouter>
          <div>
            <Header />
            <Route exact path="/" component={Home} />
          </div>
        </BrowserRouter>
      </div>
    );
  }
}

export default App;
