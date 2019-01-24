import React from 'react';
import { Paper } from '@material-ui/core';


class ParkCard extends React.Component {
    render() {
        return (
            <Paper>
                <h1>{this.props.park.name}</h1>
            </Paper>
        )
    }
}

export default ParkCard;