import React from 'react';
import FuseboxApi from './FuseboxApi';
import Track from './Track';

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
        const tracks = this.state.tracks.map((track) =>
            <Track id={track.id} artists={track.artits} album={track.album} title={track.title} />
        );

        return (
            <table className="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Artists</th>
                        <th scope="col">Title</th>
                        <th scope="col">Album</th>
                        <th scope="col">Rate</th>
                    </tr>
                </thead>
                <tbody>
                    {tracks}
                </tbody>
            </table>
        )
    }
}

export default Rate;