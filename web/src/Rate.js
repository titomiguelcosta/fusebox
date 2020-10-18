import React from 'react';
import FuseboxApi from './FuseboxApi';

class Rate extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            unratedTracks: []
        }
        this.api = new FuseboxApi();
    }

    componentDidMount() {
        if (this.api.getAccessToken()) {
            this.api.unratedTracks().then(tracks => {
                window.console.log(tracks);

                this.setState({
                    unratedTracks: tracks
                });
            });
        }
    }

    render() {
        const tracks = this.state.unratedTracks.map((track, item) =>
            <div key={item}> {track.album}: {track.title}</div>
        );

        return (
            <div className="App">
                <header className="App-header">
                    {tracks}
                </header>
            </div>
        )
    }
}

export default Rate;