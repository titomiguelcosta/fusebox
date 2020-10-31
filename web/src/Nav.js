import React from 'react';
import Login from './Login';
import { Link } from "react-router-dom";

class Nav extends React.Component {
    render() {
        return (
            <nav className="navbar navbar-expand-md fixed-top">
                <a className="navbar-brand" href="/">Fusebox</a>
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault"
                    aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarsExampleDefault">
                    <ul className="navbar-nav mr-auto">
                        <li className="nav-item">
                            <Link className="nav-link" to="/rate">Rate</Link>
                        </li>
                        <li className="nav-item dropdown">
                            <a className="nav-link dropdown-toggle" href="?#" id="dropdown01" data-toggle="dropdown"
                                aria-haspopup="true" aria-expanded="false">Login</a>
                            <Login />
                        </li>
                    </ul>
                </div>
                <form method="get" action="/search" className="form-inline my-2 my-lg-0">
                    <input name="q" className="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search"></input>
                    <button className="btn btn-outline-primary my-2 my-sm-0" type="submit">Search</button>
                </form>
            </nav>
        )
    }
}

export default Nav;