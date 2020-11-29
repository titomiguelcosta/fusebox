import React from 'react';
import FuseboxApiClient from '../FuseboxApi';
import { Link } from "react-router-dom";
import Rate from './Rate';

class Track extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            deleted: false,
        }
    }

    handleDelete(e) {
        e.preventDefault();
        FuseboxApiClient
            .deleteTrack(this.props.id)
            .then(response => {
                this.setState({
                    deleted: 204 === response.status
                });
            });
    }

    render() {
        const artists = this.props.artists.map((artist, i) => {
            return (
                <>
                    <Link
                        key={artist}
                        to={{ pathname: '/search', search: "?q=" + artist }}
                    >
                        {artist}
                    </Link>
                    { this.props.artists[i + 1] ? <span>, </span> : <></>}
                </>
            );
        });

        return (
            this.state.deleted
                ? <></>
                :
                <tr key={this.props.id}>
                    <td>{artists}</td>
                    <td>
                        <Link
                            to={{
                                pathname: "/tracks/" + this.props.id
                            }}>{this.props.title}
                        </Link>
                    </td>
                    <td>{this.props.album}</td>
                    <td>
                        <div className="btn-group" role="group" aria-label="Actions">
                            <Rate id={this.props.id} />
                            <button onClick={(e) => this.handleDelete(e)} type="button" className="btn btn-danger">Delete</button>
                        </div>
                    </td>
                </tr>
        );
    }
}

export default Track;