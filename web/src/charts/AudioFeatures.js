import React from 'react';
import FuseboxApi from './../FuseboxApi';
import {
    Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Legend, Tooltip
} from 'recharts';

class AudioFeatures extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            data: []
        };

        this.api = new FuseboxApi();
    }

    componentDidMount() {
        if (this.api.getAccessToken()) {
            this.api.statsAudioFeatures(this.props.id).then((json) => {
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
                <div className="row">
                    <div className="col-sm">
                        <RadarChart
                            width={600}
                            height={220}
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
                    </div>
                </div>
                : ''
        );
    }
}

export default AudioFeatures;
