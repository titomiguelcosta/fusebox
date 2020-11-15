import React from 'react';
import FuseboxApi from '../FuseboxApi';
import { Link } from "react-router-dom";
import Rate from './Rate';

class Track extends React.Component {
    constructor(props) {
        super(props);

        this.api = new FuseboxApi();
    }

    render() {
        return (
            <tr>
                <td>{this.props.artists.join(', ')}</td>
                <td>
                    <Link
                        to={{
                            pathname: "/tracks/" + this.props.id
                        }}>{this.props.title}
                    </Link>
                </td>
                <td>{this.props.album}</td>
                <td>
                    <div className="dropdown">
                        <Rate id={this.props.id} />
                    </div>
                </td>
            </tr>
        );
    }
}

export default Track;