import React from 'react';
import FuseboxApi from './../FuseboxApi';
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
} from 'recharts';

class TracksPerRate extends React.Component {
    constructor(props) {
        super(props);

        this.api = new FuseboxApi();

        this.state = {
            data: []
        };
    }

    componentDidMount() {
        if (this.api.getAccessToken()) {
            this.api.statsTracksPerRate().then((json) => {
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
                        <BarChart
                            width={500}
                            height={300}
                            data={this.state.data}
                            margin={{
                                top: 0, right: 0, left: 0, bottom: 0,
                            }}
                        >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="rate" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="tracks" fill="#8884d8" />
                        </BarChart>
                    </div>
                </div>
                : ''
        );
    }
}

export default TracksPerRate;
