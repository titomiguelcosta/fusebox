import React from 'react';
import FuseboxApi from './FuseboxApi';
import Video from './helpers/Video';
import Rate from './helpers/Rate';
import SpotifyPlayer from 'react-spotify-player';

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

    onRating(rate) {
        let track = this.state.track;
        if (track) {
            track.rate.score = rate;
            this.setState({
                track: track,
            });
        }
    }

    render() {
        const track = this.state.track
            ? <h1>{this.state.track.title} <i>by</i> {this.state.track.artists.join(', ')} <i>from</i> {this.state.track.album}</h1>
            : <div>No details.</div>;

        const details = this.state.track
            ? <table className="table">
                <thead className="thead-dark">
                    <tr>
                        <th>danceability</th>
                        <th>energy</th>
                        <th>loudness</th>
                        <th>speechiness</th>
                        <th>acousticness</th>
                        <th>instrumentalness</th>
                        <th>liveness</th>
                        <th>valence</th>
                        <th>tempo</th>
                        <th>key</th>
                        <th>time signature</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{this.state.track.danceability}</td>
                        <td>{this.state.track.energy}</td>
                        <td>{this.state.track.loudness}</td>
                        <td>{this.state.track.speechiness}</td>
                        <td>{this.state.track.acousticness}</td>
                        <td>{this.state.track.instrumentalness}</td>
                        <td>{this.state.track.liveness}</td>
                        <td>{this.state.track.valence}</td>
                        <td>{this.state.track.tempo}</td>
                        <td>{this.state.track.key}</td>
                        <td>{this.state.track.time_signature}</td>
                    </tr>
                </tbody>
            </table>
            : '';

        const rate = this.state.track && this.state.track.rate.score
            ? 'You set a score of ' + this.state.track.rate.score
            : 'Unrated track';

        const videos = this.state.track && this.state.track.videos.length > 0
            ?
            <div id="videos" className="carousel slide" data-ride="carousel">
                <div className="carousel-inner">
                    {this.state.track.videos.map((video, index) => {
                        let itemClasses = "carousel-item" + (0 == index ? " active" : "");

                        return (
                            <div className={itemClasses} key={index}>
                                <Video url={video.url}></Video>
                            </div>
                        );
                    })}
                </div>
                <a className="carousel-control-prev" href="#videos" role="button" data-slide="prev">
                    <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span className="sr-only">Previous</span>
                </a>
                <a className="carousel-control-next" href="#videos" role="button" data-slide="next">
                    <span className="carousel-control-next-icon" aria-hidden="true"></span>
                    <span className="sr-only">Next</span>
                </a>
            </div>
            : '';

        const player = this.state.track && this.state.track.spotify_id
            ? <SpotifyPlayer
                uri={this.state.track.spotify_id}
                size='compact'
                view='coverart'
                theme='black'
            />
            : '';

        return (
            <div>
                {track}
                {details}
                <hr />

                <div className="section">
                    {rate}
                    <Rate id={this.state.id} onRating={(rate) => this.onRating(rate)} />
                </div>

                <hr />

                {player}

                <hr />

                {videos}
            </div>
        );
    }
}

export default TrackDetails;
