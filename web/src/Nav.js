import React from 'react';
import Login from './Login';
import { Link } from "react-router-dom";
import FuseboxApiClient from './FuseboxApi';

class Nav extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            authenticated: !!FuseboxApiClient.getAccessToken(),
        }
    }

    handleAuthentication() {
        window.console.log("you are now authenticated")
        this.setState({
            authenticated: true,
        });
    }

    handleLogout() {
        FuseboxApiClient.removeAccessToken();
        this.setState({
            authenticated: false,
        });
        window.console.log("you are now logged out");
    }

    handleDownload(e) {
        e.preventDefault();
        FuseboxApiClient.dumpTracks();
    }

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
                        {
                            this.state.authenticated
                                ?
                                <>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/rate">Unrated</Link>
                                    </li>
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/dashboard">Dashboard</Link>
                                    </li>
                                    <li className="nav-item">
                                        <a onClick={(e) => this.handleDownload(e)} className="nav-link" href="/#" aria-expanded="false">Download</a>
                                    </li>
                                </>
                                : ''
                        }
                        {
                            this.state.authenticated
                                ?
                                <li className="nav-item">
                                    <Link onClick={() => this.handleLogout()} className="nav-link" to="/">Logout</Link>
                                </li>
                                :
                                <li className="nav-item dropdown">
                                    <a className="nav-link dropdown-toggle" href="?#" data-toggle="dropdown"
                                        aria-haspopup="true" aria-expanded="false">Login</a>
                                    <Login onAuthentication={() => this.handleAuthentication()} />
                                </li>
                        }
                    </ul>
                </div>

                {
                    this.state.authenticated
                        ?
                        <form method="get" action="/search" className="form-inline my-2 my-lg-0">
                            <input name="q" className="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search"></input>
                            <button className="btn btn-outline-primary my-2 my-sm-0" type="submit">Search</button>
                        </form>
                        :
                        ''
                }
            </nav>
        )
    }
}

export default Nav;
