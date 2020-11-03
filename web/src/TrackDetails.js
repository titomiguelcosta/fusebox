import React from 'react';
import FuseboxApi from './FuseboxApi';
import { useParams } from "react-router-dom";


class TrackDetails extends React.Component {
    constructor(props) {
        super(props);
        this.api = new FuseboxApi();
        this.state = {
            id: useParams(),
        }
    }

    render() {
        return (
            <h1>Track details for {this.state.id}</h1>
        );
    }
}

export default TrackDetails;