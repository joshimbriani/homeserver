import React from 'react';
import { Paper, Typography, ListItem, ListItemText } from '@material-ui/core';
import { URL } from '../../utils/network';
import moment from 'moment';

function ListItemLink(props) {
    return <ListItem button component="a" {...props} />;
}

class ArticlesCard extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            articles: [],
            loading: false
        }
    }
    
    componentDidMount() {
        this.setState({ loading: true })
        fetch(URL + "api/v1/coasters/articles")
            .then(response => response.json())
            .then(responseJSON => this.setState({ articles: responseJSON, loading: false }))
    }

    render() {
        return (
            <Paper style={{ padding: 10, marginTop: 20 }}>
                <Typography
                    component="h2"
                    variant="h5"
                    color="inherit"
                    align="center"
                    noWrap
                >
                    Industry Headlines
                </Typography>
                {this.state.loading && <p>
                    Loading
                </p>}
                {this.state.articles.map((article, index) => {
                    return (
                        <ListItemLink href={article[1]} target="_blank">
                            <ListItemText primary={article[0]} secondary={moment(article[2]).format('MMMM Do YYYY, h:mm:ss a')} />
                        </ListItemLink>
                    )
                })}
            </Paper>
        )
    }
}

export default ArticlesCard;