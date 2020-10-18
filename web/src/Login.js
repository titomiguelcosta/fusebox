import React from 'react';
import FuseboxApi from './FuseboxApi';

class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
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

        this.api.auth(this.state.username, this.state.password)
            .then(response => {
                if (response['access']) {
                    this.api.setAccessToken(response['access']);
                    this.api.setRefreshToken(response['refresh']);
                    this.setState({
                        username: '',
                        password: '',
                        loggedIn: true
                    })
                }
            });
    }

    render() {
        const auth = this.state.loggedIn ? (
            <div>Hello hello!!</div>
        ) : (
                <form className="form-inline my-2 my-lg-0">
                    <input onChange={(e) => this.handleUsernameChange(e)} className="form-control mr-sm-2" type="text" placeholder="Username" aria-label="Username"></input>
                    <input onChange={(e) => this.handlePasswordChange(e)} className="form-control mr-sm-2" type="password" placeholder="Password" aria-label="Password"></input>
                    <button onClick={(e) => this.handleSubmit(e)} className="btn btn-outline-success my-2 my-sm-0" type="submit">Login</button>
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