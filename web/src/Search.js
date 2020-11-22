import React from 'react';
import FuseboxApi from './FuseboxApi';
import Track from './helpers/Track';

class Search extends React.Component {
    constructor(props) {
        super(props);
        let params = new URLSearchParams(window.location.search);
        let q = params.get('q');

        this.state = {
            searching: true,
            tracks: [],
            offset: 0,
            limit: 10,
            q: q,
        }
        this.api = new FuseboxApi();
    }

    componentDidMount() {
        this.setState({
            searching: true,
        });

        if (this.api.getAccessToken()) {
            this.api.searchTracks(this.state.q).then(tracks => {
                this.setState({
                    tracks: tracks,
                    searching: false,
                });
            });
        }
    }

    handlePrevious(e) {
        e.preventDefault();
        const newOffset = this.state.offset - this.state.limit;

        if (newOffset >= 0) {
            this.setState({
                tracks: [],
            });

            this.api.searchTracks(this.state.q, newOffset, this.state.limit).then(tracks => {
                this.setState({
                    offset: newOffset,
                    tracks: tracks,
                });
            });
        }
    }

    handleNext(e) {
        e.preventDefault();
        if (this.state.tracks.length >= this.state.limit) {
            this.setState({
                tracks: [],
            });

            const newOffset = this.state.offset + this.state.limit;

            this.api.searchTracks(this.state.q, newOffset, this.state.limit).then(tracks => {
                this.setState({
                    offset: newOffset,
                    tracks: tracks,
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
                            <a className="page-link" href="/#" tabIndex="-1" onClick={(e) => this.handlePrevious(e)}>Previous</a>
                        </li>
                        <li className={nextClasses}>
                            <a className="page-link" href="/#" onClick={(e) => this.handleNext(e)}>Next</a>
                        </li>
                    </ul>
                </nav>
            </>
        )
    }
}

export default Search;