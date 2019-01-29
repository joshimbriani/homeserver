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
            park: [],
            loading: false
        }
    }

    componentDidMount() {
        this.setState({ loading: true })
        fetch(URL + "api/v1/screamscape")
            .then(response => response.json())
            .then(responseJSON => this.setState({ articles: responseJSON, loading: false }))
    }

    render() {
        return (
            <Paper style={{ padding: 10 }}>
                <Typography
                    component="h2"
                    variant="h5"
                    color="inherit"
                    align="center"
                    noWrap
                >
                    Screamscape Headlines
                </Typography>
                {this.state.loading && <p>
                    Loading
                </p>}
                {this.state.articles.map((article, index) => {
                    return (
                        <ListItemLink href={article[1]} target="_blank">
                            <ListItemText primary={article[0]} />
                        </ListItemLink>
                    )
                })}
            </Paper>
        )
    }
}

ParkCard.propTypes = {
    park: PropTypes.string
};

export default ParkCard;