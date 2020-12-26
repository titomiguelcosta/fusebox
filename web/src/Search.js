import React from 'react';
import FuseboxApiClient from './FuseboxApi';
import Track from './helpers/Track';
import { Link } from "react-router-dom";

class Search extends React.Component {
    constructor(props) {
        super(props);
        let params = new URLSearchParams(window.location.search);
        let q = params.get('q');

        this.state = {
            searching: false,
            tracks: [],
            offset: parseInt(params.get('offset')) || 0,
            limit: 10,
            q: q,
        }
    }

    componentDidMount() {
        if (!this.state.searching) {
            this.setState({
                searching: true,
            });

            FuseboxApiClient.searchTracks(this.state.q, this.state.offset, this.state.limit).then(tracks => {
                this.setState({
                    tracks: tracks,
                    searching: false,
                });
            });
        }
    }

    render() {
        const title = this.state.searching
            ? "Searching for " + this.state.q
            : "Results for " + this.state.q;

        const tracks = this.state.tracks.map((track) =>
            <Track key={track.id} id={track.id} artists={track.artists} album={track.album} title={track.title} />
        );

        const previousClasses = "page-item" + (this.state.offset === 0 ? " disabled" : "");
        const nextClasses = "page-item" + (this.state.tracks.length < this.state.limit ? " disabled" : "");

        return (
            <>
                <table className="table table-hover">
                    <caption>{title}</caption>
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

                <nav aria-label="navigation" className="d-flex justify-content-end">
                    <ul className="pagination">
                        <li className={previousClasses}>
                            <Link
                                className="page-link"
                                to={"/search?q=" + this.state.q + "&offset=" + (this.state.offset - this.state.limit)}
                                tabIndex="-1"
                                onClick={() => { this.setState({ offset: (this.state.offset - this.state.limit) }) }}>
                                Previous
                            </Link>
                        </li>
                        <li className={nextClasses}>
                            <Link
                                className="page-link"
                                to={"/search?q=" + this.state.q + "&offset=" + (this.state.offset + this.state.limit)}
                                onClick={() => { this.setState({ offset: (this.state.offset + this.state.limit) }) }}>
                                Next
                            </Link>
                        </li>
                    </ul>
                </nav>
            </>
        )
    }
}

export default Search;