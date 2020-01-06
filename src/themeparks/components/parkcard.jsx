import React from 'react';
import { Paper, Typography, ListItem, Divider, Grid } from '@material-ui/core';
import { URL } from '../../utils/network';
import PropTypes from 'prop-types';

function ListItemLink(props) {
    return <ListItem button component="a" {...props} />;
}

class ParkCard extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            park: {},
            loadingPark: false,
            loadingWaitTimes: false,
            waitTimes: [],
            rideChoices: []
        }
    }

    componentDidMount() {
        this.setState({ loadingPark: true, loadingWaitTimes: true })
        fetch(URL + "api/v1/coasters/parks/?one=true&abbrev=" + this.props.park)
            .then(response => response.json())
            .then(responseJSON => {
                this.setState({ park: responseJSON, loadingPark: false });
                fetch(URL + "api/v1/coasters/parks/" + responseJSON["id"])
                    .then(responsewaittime => responsewaittime.json())
                    .then(responsewaittimesJSON => {
                        console.log(responsewaittimesJSON)
                        var rideChoices = [];
                        for (var i = 0; i < 4; i++) {
                            rideChoices.push(getRideByIndex(responsewaittimesJSON.rides, Math.floor(Math.random() * responsewaittimesJSON.rides.length)))
                        }
                        this.setState({ waitTimes: responsewaittimesJSON, loadingWaitTimes: false, rideChoices: rideChoices })
                    });
            });
    }

    renderWaitTimeCard(ride) {

    }

    render() {
        console.log(this.state)
        return (
            <Paper>
                {this.state.loading && <p>
                    Loading
                </p>}
                {Object.keys(this.state.park).length > 0 && <div>
                    <Typography variant="h5">
                        {this.state.park.name}
                    </Typography>
                    <Typography variant="overline">
                        Busier Than Normal
                    </Typography>
                    <Divider />
                    <Typography variant="overline">
                        Wait Times
                    </Typography>
                    <Grid container spacing={24}>
                        {this.state.rideChoices.map(ride => {
                            return (
                                <Grid item xs={3}>
                                    <Paper className={{ padding: 10 }}>
                                        <Typography variant="overline">
                                            {ride.name}
                                        </Typography>
                                    </Paper>
                                </Grid>
                            )
                        })}
                    </Grid>
                </div>}
            </Paper>
        )
    }
}

function getRideByIndex(rides, index) {
    for (var i = 0; i < rides.length; i++) {
        if (i === index) {
            return rides[i];
        }
    }

    return -1;
}

ParkCard.propTypes = {
    park: PropTypes.string
};

export default ParkCard;