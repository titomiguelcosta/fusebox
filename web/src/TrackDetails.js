import React from 'react';
import FuseboxApiClient from './FuseboxApi';
import Video from './helpers/Video';
import Rate from './helpers/Rate';
import SpotifyPlayer from 'react-spotify-player';
import AudioFeatures from './charts/AudioFeatures';

class TrackDetails extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            id: this.props.match.params.id,
            track: null,
            predictions: null,
        }
    }

    componentDidMount() {
        if (FuseboxApiClient.getAccessToken()) {
            FuseboxApiClient.detailsTrack(this.state.id).then(track => {
                this.setState({
                    track: track,
                });
            });
            FuseboxApiClient.predictionsTrack(this.state.id).then(predictions => {
                this.setState({
                    predictions: predictions.predictions,
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
            ?
            <ul>
                <li>danceability: {this.state.track.danceability}</li>
                <li>energy: {this.state.track.energy}</li>
                <li>loudness: {this.state.track.loudness}</li>
                <li>speechiness: {this.state.track.speechiness}</li>
                <li>acousticness: {this.state.track.acousticness}</li>
                <li>instrumentalness: {this.state.track.instrumentalness}</li>
                <li>liveness: {this.state.track.liveness}</li>
                <li>valence: {this.state.track.valence}</li>
                <li>tempo: {this.state.track.tempo}</li>
                <li>key: {this.state.track.key}</li>
                <li>time signature: {this.state.track.time_signature}</li>
            </ul>
            : '';

        const predictions = this.state.predictions
            ?
            <>
                <h3>Regression</h3> 
                <dl>
                    {this.state.predictions.regression.map(prediction => {
                        return (
                            <>
                                <dt>{prediction.model}</dt>
                                <dd>{prediction.score}</dd>
                            </>
                        );
                    })}
                </dl>
                <h3>Binary</h3>
                <dl>
                    {this.state.predictions.classification.binary.map(prediction => {
                        return (
                            <>
                                <dt>{prediction.model}</dt>
                                <dd>{prediction.score ? 'You like it' : 'Not your cup of tea'}</dd>
                            </>
                        );
                    })}
                </dl>

                <h3>Multiclass</h3>
                <dl>
                    {this.state.predictions.classification.multiclass.map(prediction => {
                        return (
                            <>
                                <dt>{prediction.model}</dt>
                                <dd>{prediction.score}</dd>
                            </>
                        );
                    })}
                </dl>
            </>
            : '';

        const rate = this.state.track && this.state.track.rate.score
            ? 'You set a score of ' + this.state.track.rate.score
            : 'Unrated track';

        const videos = this.state.track && this.state.track.videos.length > 0
            ?
            <div id="videos" className="carousel slide" data-ride="carousel">
                <div className="carousel-inner">
                    {this.state.track.videos.map((video, index) => {
                        let itemClasses = "carousel-item" + (0 === index ? " active" : "");

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
                <hr />

                <div className="card">
                    <div className="card-header">Audio features</div>
                    <div className="card-body row">
                        <div className="col-sm">
                            <AudioFeatures id={this.state.id} />
                        </div>
                        <div className="col-sm">
                            {details}
                        </div>
                    </div>
                </div>

                <hr />

                <div className="section">
                    <h2>Rating</h2>

                    {rate}

                    <Rate id={this.state.id} onRating={(rate) => this.onRating(rate)} />
                </div>

                <hr />

                <h2>Predictions</h2>
                {predictions}

                <hr />

                {player}

                <hr />

                {videos}
            </div>
        );
    }
}

export default TrackDetails;
