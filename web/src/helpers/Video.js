import React from 'react';
import ReactPlayer from 'react-player'

class Video extends React.Component {
    render() {
        return <ReactPlayer url={this.props.url} width="400" height="260" />;
    }
}

export default Video;
