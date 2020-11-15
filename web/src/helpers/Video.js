import React from 'react';
import ReactPlayer from 'react-player'

class Video extends React.Component {
    render() {
        return <ReactPlayer url={this.props.url} controls={true} width="100%" height="320px" />;
    }
}

export default Video;
