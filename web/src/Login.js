import React from 'react';
import FuseboxApi from './FuseboxApi';

class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            authenticating: false,
            errors: false,
            loggedIn: false
        }
        this.api = new FuseboxApi();
    }

    componentDidMount() {
        if (this.api.getAccessToken()) {
            this.setState({
                loggedIn: true
            });
        }
    }

    handleUsernameChange(e) {
        this.setState({
            username: e.target.value
        });
    }

    handlePasswordChange(e) {
        this.setState({
            password: e.target.value
        });
    }

    handleSubmit(e) {
        e.preventDefault();

        this.setState({
            authenticating: true
        })

        this.api.auth(this.state.username, this.state.password)
            .then(response => {
                if (response['access']) {
                    this.api.setAccessToken(response['access']);
                    this.api.setRefreshToken(response['refresh']);
                    this.setState({
                        username: '',
                        password: '',
                        loggedIn: true,
                        errors: false,
                        authenticating: false
                    });
                } else {
                    this.setState({
                        errors: true,
                        authenticating: false
                    });
                }
            });
    }

    render() {
        const authenticationButton = this.state.authenticating ? (
            <button className="btn btn-primary" type="button" disabled>
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <span class="sr-only">Authenticating...</span>
            </button>
        ) : (
                <button onClick={(e) => this.handleSubmit(e)} className="btn btn-primary my-2 my-sm-0" type="submit">Login</button>
            );

        const errorMessage = this.state.errors ? (
            (<div class="alert alert-danger">Failed to authenticate</div>)
        ) : (<></>);

        const auth = this.state.loggedIn ? (
            <div>Hello hello!!</div>
        ) : (
                <form className="form-inline my-2 my-lg-0" >
                    {errorMessage}

                    <input onChange={(e) => this.handleUsernameChange(e)} className="form-control mr-sm-2" type="text" placeholder="Username" aria-label="Username"></input>
                    <input onChange={(e) => this.handlePasswordChange(e)} className="form-control mr-sm-2" type="password" placeholder="Password" aria-label="Password"></input>

                    {authenticationButton}
                </form>
            );

        return (
            <div className="dropdown-menu" aria-labelledby="dropdown01">
                {auth}
            </div>
        );
    }
}

export default Login;