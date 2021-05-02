import React, { Component } from 'react';
import './App.css';
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import IndexPage from "./Pages/IndexPage/IndexPage"
import axios from 'axios'
import { CookiesProvider, withCookies } from 'react-cookie';
import config from './config'

class App extends Component {
  constructor(props) {
    super(props)
    const tokenId = this.props.cookies.get(config.login_cookie_name)
    if (tokenId) {
      axios.defaults.headers.common['X-CSRF-TOKEN'] = tokenId;
    }
  }

  componentDidCatch(error) {
    // Handling errors globally
    console.log(error)
  }

  render() {
    return (
      <CookiesProvider>
          <Router>
            <Switch>
              <Route exact path="/">
                <IndexPage />
              </Route>
            </Switch>
          </Router>
      </CookiesProvider>
    );
  }
}

export default withCookies(App);
