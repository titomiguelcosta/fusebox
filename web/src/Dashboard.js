import React from 'react';
import {
    ResponsiveContainer,
    LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip,
    BarChart, Bar, Legend
} from 'recharts';

class Dashboard extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const data = [
            { name: 'Page A', uv: 400, pv: 2400, amt: 2400 },
            { name: 'Page B', uv: 300, pv: 2100, amt: 2700 },
            { name: 'Page C', uv: 200, pv: 100, amt: 700 },
        ];

        return (
            <ResponsiveContainer>
                <div className="row">
                    <div className="col-sm">
                        <LineChart width={500} height={300} data={data}>
                            <Line type="monotone" dataKey="uv" stroke="#8884d8" />
                            <Line type="monotone" dataKey="pv" stroke="#8884d8" />
                            <Line type="monotone" dataKey="amt" stroke="#8884d8" />
                            <CartesianGrid stroke="#ccc" />
                            <XAxis dataKey="Page" />
                            <YAxis />
                            <Tooltip />
                        </LineChart>
                    </div>
                    <div className="col-sm">
                        <BarChart
                            width={500}
                            height={300}
                            data={data}
                            margin={{
                                top: 5, right: 30, left: 20, bottom: 5,
                            }}
                        >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="pv" fill="#8884d8" />
                            <Bar dataKey="uv" fill="#82ca9d" />
                        </BarChart>
                    </div>
                </div>
            </ResponsiveContainer>
        );
    }
}

export default Dashboard;
