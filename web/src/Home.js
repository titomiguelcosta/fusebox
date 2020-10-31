import React from 'react';
import logo from './logo.png';

class Home extends React.Component {
    render() {
        return (
            <>
                <div className="jumbotron">
                    <div className="media">
                        <div class="media-left">
                            <img src={logo} alt="Fusebox" width="185" />
                        </div>
                        <div class="media-body">
                            <h1>Fusebox</h1>
                            <p>music recommendation system</p>
                        </div>
                    </div>
                </div>

                <div className="row">
                    <div className="col">
                        <h2>Product</h2>
                        <p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p>
                        <p><a className="btn" href="#">View details »</a></p>
                    </div>
                    <div className="col">
                        <h2>Suggestions</h2>
                        <p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. </p>
                        <p><a className="btn" href="#">View details »</a></p>
                    </div>
                    <div className="col">
                        <h2>Integrations</h2>
                        <p>Donec sed odio dui. Cras justo odio, dapibus ac facilisis in, egestas eget quam. Vestibulum id ligula porta felis euismod semper. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.</p>
                        <p><a className="btn" href="#">View details »</a></p>
                    </div>
                </div>
            </>
        )
    }
}

export default Home;