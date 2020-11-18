import React from 'react';
import TracksPerRate from './charts/TracksPerRate';
import RatePerArtist from './charts/RatePerArtist';
import TracksPerArtist from './charts/TracksPerArtist';

class Dashboard extends React.Component {

    render() {
        return (
            <>
                <RatePerArtist />
                <TracksPerRate />
                <TracksPerArtist />
            </>
        );
    }
}

export default Dashboard;
