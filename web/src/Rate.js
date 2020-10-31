import React from 'react';
import FuseboxApi from './FuseboxApi';

class Rate extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tracks: [],
        }
        this.api = new FuseboxApi();
    }

    componentDidMount() {
        if (this.api.getAccessToken()) {
            this.api.unratedTracks().then(tracks => {
                this.setState({
                    tracks: tracks
                });
            });
        }
    }

    render() {
        const tracks = this.state.tracks.map((track, item) =>
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