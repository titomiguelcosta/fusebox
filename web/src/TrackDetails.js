import React from 'react';
import FuseboxApi from './FuseboxApi';

class TrackDetails extends React.Component {
    constructor(props) {
        super(props);
        this.api = new FuseboxApi();
        this.state = {
            id: this.props.match.params.id,
        }
    }

    render() {
        return (
            <h1>Track details for track with id {this.state.id}</h1>
        );
    }
}

export default TrackDetails;