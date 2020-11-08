import React from 'react';
import FuseboxApi from './FuseboxApi';

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

        return (
            <>{track}</>
        );
    }
}

export default TrackDetails;