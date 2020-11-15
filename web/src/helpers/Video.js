import React from 'react';
import ReactPlayer from 'react-player'

class Video extends React.Component {
    render() {
        return <ReactPlayer url={this.props.url} controls="true" width="410" height="320" />;
    }
}

export default Video;
