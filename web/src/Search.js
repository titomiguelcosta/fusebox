import React from 'react';
import FuseboxApi from './FuseboxApi';

class Search extends React.Component {
    constructor(props) {
        super(props);
        let params = new URLSearchParams(window.location.search);
        let q = params.get('q');

        this.state = {
            searching: true,
            tracks: [],
            q: q
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

    render() {
        const title = this.state.searching
            ? "Searching for " + this.state.q
            : "Results for " + this.state.q
            ;

        const tracks = this.state.tracks.map((track, item) =>
            <div key={item}> {track.album}: {track.title}</div>
        );

        return (
            <div className="App">
                <header className="App-header">
                    {title}
                </header>
                <section>
                    {tracks}
                </section>
            </div>
        )
    }
}

export default Search;