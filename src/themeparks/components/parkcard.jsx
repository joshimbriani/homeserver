import React from 'react';
import { Paper, Typography, ListItem, ListItemText } from '@material-ui/core';
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
            waitTimes: []
        }
    }

    componentDidMount() {
        this.setState({ loadingPark: true, loadingWaitTimes: true })
        fetch(URL + "api/v1/coasters/parks/?one=true&abbrev=" + this.props.park)
            .then(response => response.json())
            .then(responseJSON => {
                this.setState({ park: responseJSON, loadingPark: false });
                fetch(URL + "api/v1/coasters/waittimes/" + responseJSON["id"])
                    .then(responsewaittime => responsewaittime.json())
                    .then(responsewaittimesJSON => this.setState({ waitTimes: responsewaittimesJSON, loadingWaitTimes: false }));
            });
    }

    render() {
        return (
            <Paper style={[{ padding: 10 }, this.props.style]}>
                {this.state.loading && <p>
                    Loading
                </p>}
                {Object.keys(this.state.park).length > 0 && <div>
                    <Typography variant="h5" gutterBottom>
                        {this.state.park.name}
                    </Typography>
                    <Typography variant="overline" gutterBottom>
                        Busier Than Normal
                    </Typography>
                </div>}
            </Paper>
        )
    }
}

ParkCard.propTypes = {
    park: PropTypes.string
};

export default ParkCard;