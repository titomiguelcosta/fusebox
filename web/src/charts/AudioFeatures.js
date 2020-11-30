import React from 'react';
import FuseboxApiClient from './../FuseboxApi';
import {
    Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Legend, Tooltip, ResponsiveContainer
} from 'recharts';

class AudioFeatures extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            data: []
        };

    }

    componentDidMount() {
        if (FuseboxApiClient.getAccessToken()) {
            FuseboxApiClient.statsAudioFeatures(this.props.id).then((json) => {
                this.setState({
                    data: json["results"]
                });
            });
        }
    }

    render() {
        return (
            this.state.data
                ?
                <ResponsiveContainer width="100%" height={260}>
                    <RadarChart
                        data={this.state.data}
                        margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
                    >
                        <PolarGrid />
                        <PolarAngleAxis dataKey="name" />
                        <PolarRadiusAxis />
                        <Radar name="Audio Features" dataKey="value" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                        <Legend />
                        <Tooltip />
                    </RadarChart>
                </ResponsiveContainer>
                : ''
        );
    }
}

export default AudioFeatures;
