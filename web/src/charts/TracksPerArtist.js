import React from 'react';
import FuseboxApiClient from './../FuseboxApi';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

class TracksPerArtist extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            data: []
        };

    }

    componentDidMount() {
        if (FuseboxApiClient.getAccessToken()) {
            FuseboxApiClient.statsTracksPerArtist().then((json) => {
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
                <div className="card">
                    <div className="card-header">Number of tracks per artist</div>
                    <div className="card-body">
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart
                                width={500}
                                height={300}
                                data={this.state.data}
                                margin={{
                                    top: 0, right: 0, left: 0, bottom: 0,
                                }}
                            >
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="tracks" fill="#8884d8" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
                : ''
        );
    }
}

export default TracksPerArtist;
