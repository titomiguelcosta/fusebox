import React from 'react';
import FuseboxApiClient from '../FuseboxApi';

class Rate extends React.Component {
    handleRate(e, rate) {
        e.preventDefault();

        FuseboxApiClient.rateTrack(this.props.id, rate);

        if (this.props.onRating) {
            this.props.onRating(rate);
        }
    }

    render() {
        return (
            <div className="dropdown">
                <button className="btn btn-secondary dropdown-toggle" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Rate</button>
                <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    <a className="dropdown-item" href="/#" onClick={(e) => this.handleRate(e, 0)}>0</a>
                    <a className="dropdown-item" href="/#" onClick={(e) => this.handleRate(e, 1)}>1</a>
                    <a className="dropdown-item" href="/#" onClick={(e) => this.handleRate(e, 2)}>2</a>
                    <a className="dropdown-item" href="/#" onClick={(e) => this.handleRate(e, 3)}>3</a>
                    <a className="dropdown-item" href="/#" onClick={(e) => this.handleRate(e, 4)}>4</a>
                    <a className="dropdown-item" href="/#" onClick={(e) => this.handleRate(e, 5)}>5</a>
                    <a className="dropdown-item" href="/#" onClick={(e) => this.handleRate(e, 6)}>6</a>
                    <a className="dropdown-item" href="/#" onClick={(e) => this.handleRate(e, 7)}>7</a>
                    <a className="dropdown-item" href="/#" onClick={(e) => this.handleRate(e, 8)}>8</a>
                    <a className="dropdown-item" href="/#" onClick={(e) => this.handleRate(e, 9)}>9</a>
                    <a className="dropdown-item" href="/#" onClick={(e) => this.handleRate(e, 10)}>10</a>
                </div>
            </div>
        );
    }
}

export default Rate;