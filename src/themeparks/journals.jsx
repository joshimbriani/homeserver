import React from 'react';
import { Grid, Paper, Typography, Divider, Button, Card, CardActionArea, CardMedia, CardContent, CardActions } from '@material-ui/core';
import { URL } from '../utils/network';
import { Link, Redirect } from "react-router-dom";
import Markdown from 'react-remarkable';
import moment from 'moment';

const styles = {
    media: {
        // ⚠️ object-fit is not supported by IE 11.
        objectFit: 'cover',
    },
};

class Journals extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            journals: [],
            clicked: -1,
            redirectTo: false
        }
    }

    componentDidMount() {
        this.setState({ loading: true })
        fetch(URL + "api/v1/coasters/journals/")
            .then(response => response.json())
            .then(responseJSON => {
                console.log()
                this.setState({ journals: responseJSON.sort((a, b) => (a.datetime > b.datetime) ? 1 : ((b.datetime > a.datetime) ? -1 : 0)), loading: false })
            })
    }

    truncate(st) {
        if (st.length > 200) {
            return st.substring(0, 201) + " ...";
        }

        return st
    }

    renderCard(journal) {
        return (
            <Card style={styles.card}>
                <CardActionArea onClick={() => this.setState({ clicked: journal.id, redirectTo: true })}>
                    <CardMedia
                        component="img"
                        alt={journal.title}
                        style={styles.media}
                        height="140"
                        image={"/static/uploads/journalEntry/" + journal.id + ".jpeg"}
                        title={journal.title}
                    />
                    <CardContent>
                        <Typography variant="h4" paragraph>
                                {journal.title}
                        </Typography>
                        <Typography variant="caption" paragraph>
                            {moment(journal.datetime).format('dddd MMMM Do YYYY')}
                        </Typography>
                        <Markdown>
                            {this.truncate(journal.content)}
                        </Markdown>
                    </CardContent>
                </CardActionArea>
                <CardActions>
                    <Button size="small" color="primary" component={Link} to={"/themeparks/journals/" + journal.id + '?edit=true'}>
                        Edit
                    </Button>
                </CardActions>
            </Card>
        )
    }

    render() {
        if (this.state.redirectTo) {
            return (
                <Redirect push to={"/themeparks/journals/" + this.state.clicked} />
            )
        } else {
            return (
                <Paper style={{ padding: 10 }}>
                    <Typography variant="h5" component="h2" paragraph>
                        Park Journal Entries
                    </Typography>
                    <Grid container spacing={24}>
                        {this.state.journals.map((journal, index) => {
                            return (
                                <Grid item xs={6}>
                                    {this.renderCard(journal)}
                                </Grid>
                            )
                        })}
                        {this.state.journals.length <= 0 && <Typography style={{ margin: 20 }} variant="body1" component="p">
                            No Journal Entries
                        </Typography>}
                    </Grid>
                </Paper>
            )
        }

    }
}

export default Journals;