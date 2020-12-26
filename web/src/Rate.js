import React from 'react';
import FuseboxApiClient from './FuseboxApi';
import Track from './helpers/Track';
import { Link } from "react-router-dom";

class Rate extends React.Component {
    constructor(props) {
        super(props);
        let params = new URLSearchParams(window.location.search);

        this.state = {
            offset: parseInt(params.get('offset')) || 0,
            limit: 10,
            tracks: [],
        }
    }

    componentDidMount() {
        FuseboxApiClient.unratedTracks(this.state.offset, this.state.limit).then(tracks => {
            this.setState({
                tracks: tracks
            });
        });
    }

    render() {
        const tracks = this.state.tracks.map((track) =>
            <Track key={track.id} id={track.id} artists={track.artists} album={track.album} title={track.title} />
        );

        const previousClasses = "page-item" + (this.state.offset === 0 ? " disabled" : "");
        const nextClasses = "page-item" + (this.state.tracks.length < this.state.limit ? " disabled" : "");

        return (
            <>
                <table className="table table-hover">
                    <thead>
                        <tr>
                            <th scope="col">Artists</th>
                            <th scope="col">Title</th>
                            <th scope="col">Album</th>
                            <th scope="col">Actions</th>
                        </tr>
                    </thead>
                    <tbody>{tracks}</tbody>
                </table>

                <nav aria-label="navigation">
                    <ul className="pagination justify-content-end">
                        <li key="previous" className={previousClasses}>
                            <Link
                                onClick={() => this.setState({ tracks: [], offset: (this.state.offset - this.state.limit) })}
                                className="page-link"
                                to={"/rate?offset=" + (this.state.offset - this.state.limit)}
                                tabIndex="-1">
                                Previous
                                </Link>
                        </li>
                        <li key="next" className={nextClasses}>
                            <Link
                                onClick={() => {
                                    window.console.log("clicked");
                                    this.setState({ tracks: [], offset: (this.state.offset + this.state.limit) })
                                }}
                                className="page-link"
                                to={"/rate?offset=" + (this.state.offset + this.state.limit)}>
                                Next
                            </Link>
                        </li>
                    </ul>
                </nav>
            </>
        )
    }
}

export default Rate;