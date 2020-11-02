import React from 'react';
import FuseboxApi from './FuseboxApi';

class Track extends React.Component {
    constructor(props) {
        super(props);

        this.api = new FuseboxApi();
    }

    handleRate(e, rate) {
        e.preventDefault();

        this.api.rateTrack(this.props.id, rate);
    }

    render() {
        <tr>
            <td>{this.props.artists}</td>
            <td>{this.props.title}</td>
            <td>{this.props.album}</td>
            <td>
                <div className="dropdown">
                    <button className="btn btn-secondary dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Rate</button>
                    <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                        <a className="dropdown-item" href="#" onClick={(e) => this.handleRate(e, 0)}>0</a>
                        <a className="dropdown-item" href="#" onClick={(e) => this.handleRate(e, 1)}>1</a>
                        <a className="dropdown-item" href="#" onClick={(e) => this.handleRate(e, 2)}>2</a>
                        <a className="dropdown-item" href="#" onClick={(e) => this.handleRate(e, 3)}>3</a>
                        <a className="dropdown-item" href="#" onClick={(e) => this.handleRate(e, 4)}>4</a>
                        <a className="dropdown-item" href="#" onClick={(e) => this.handleRate(e, 5)}>5</a>
                        <a className="dropdown-item" href="#" onClick={(e) => this.handleRate(e, 6)}>6</a>
                        <a className="dropdown-item" href="#" onClick={(e) => this.handleRate(e, 7)}>7</a>
                        <a className="dropdown-item" href="#" onClick={(e) => this.handleRate(e, 8)}>8</a>
                        <a className="dropdown-item" href="#" onClick={(e) => this.handleRate(e, 9)}>9</a>
                        <a className="dropdown-item" href="#" onClick={(e) => this.handleRate(e, 10)}>10</a>
                    </div>
                </div>
            </td>
        </tr>
    }
}

export default Track;