import React from 'react';
import FuseboxApi from './FuseboxApi';
import Track from './Track';

class Rate extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            offset: 0,
            limit: 10,
            tracks: [],
        }
        this.api = new FuseboxApi();
    }

    componentDidMount() {
        if (this.api.getAccessToken()) {
            this.api.unratedTracks(this.state.offset, this.state.limit).then(tracks => {
                this.setState({
                    tracks: tracks
                });
            });
        }
    }

    handlePrevious(e) {
        e.preventDefault();
        const newOffset = this.state.offset - this.state.limit;

        if (newOffset >= 0) {
            this.api.unratedTracks(newOffset, this.state.limit).then(tracks => {
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
            const newOffset = this.state.offset + this.state.limit;

            this.api.unratedTracks(newOffset, this.state.limit).then(tracks => {
                this.setState({
                    offset: newOffset,
                    tracks: tracks,
                });
            });
        }
    }

    render() {
        const tracks = this.state.tracks.map((track) =>
            <Track id={track.id} artists={track.artists} album={track.album} title={track.title} />
        );

        const previousClasses = "page-item" + (this.state.offset === 0 ? "disabled" : "");
        const nextClasses = "page-item" + (this.state.tracks.length < this.state.limit ? "disabled" : "");

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
                    <tbody>
                        {tracks}
                    </tbody>
                </table>

                <nav aria-label="navigation">
                    <ul className="pagination justify-content-end">
                        <li className={previousClasses}>
                            <a className="page-link" href="/#" tabindex="-1" onClick={(e) => this.handlePrevious(e)}>Previous</a>
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

export default Rate;