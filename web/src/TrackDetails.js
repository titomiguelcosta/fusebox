import React from 'react';
import FuseboxApi from './FuseboxApi';
import Video from './helpers/Video';
import Rate from './helpers/Rate';

class TrackDetails extends React.Component {
    constructor(props) {
        super(props);
        this.api = new FuseboxApi();
        this.state = {
            id: this.props.match.params.id,
            track: null,
        }
    }

    componentDidMount() {
        if (this.api.getAccessToken()) {
            this.api.detailsTrack(this.state.id).then(track => {
                this.setState({
                    track: track
                });
            });
        }
    }

    render() {
        const track = this.state.track
            ? <div>Details for track {this.state.track.title}</div>
            : <div>No details.</div>;

        const rate = this.state.track && this.state.track.rate.score
            ? 'You set a score of ' + this.state.track.rate.score
            : 'Unrated track';

        const videos = this.state.track
            ? this.state.track.videos.map((video) => {
                return <Video url={video.url}></Video>;
            })
            : '';

        return (
            <div>
                {track}
                <hr />
                <div className="section">
                    {rate}
                    <Rate id={this.state.id} />
                </div>
                <hr />
                {videos}
            </div>
        );
    }
}

export default TrackDetails;
