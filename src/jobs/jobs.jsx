import React from 'react';
import { Grid, Paper, Typography, Divider, Button, Card, CardActionArea, CardMedia, CardContent, CardActions } from '@material-ui/core';
import { URL } from '../utils/network';
import { Line } from 'rc-progress';
import { Link, Redirect } from "react-router-dom";
import DocumentTitle from 'react-document-title';

const styles = {
    media: {
        // ⚠️ object-fit is not supported by IE 11.
        objectFit: 'cover',
    },
};

class Jobs extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            activeJobs: [],
            inactiveJobs: [],
            completedGoals: [],
            clicked: -1,
            redirectTo: false
        }
    }

    componentDidMount() {
        this.setState({ loading: true })
        fetch(URL + "api/v1/jobs/")
            .then(response => response.json())
            .then(responseJSON => {
                var active = [];
                var inactive = [];

                for (var i = 0; i < responseJSON.length; i++) {
                    if (responseJSON[i]["active"]) {
                        active.push(responseJSON[i]);
                    } else {
                        inactive.push(responseJSON[i]);
                    }
                }

                this.setState({ activeJobs: active, inactiveJobs: inactive, loading: false })
            })
    }

    renderCard(job) {
        return (
            <Card style={styles.card}>
                <CardActionArea onClick={() => this.setState({ clicked: job.id, redirectTo: true })}>
                    <CardContent>
                        <Typography gutterBottom variant="h5" component="h2">
                            {job.name}
                        </Typography>
                        <Typography component="p">
                            {job.description}
                        </Typography>
                    </CardContent>
                </CardActionArea>
                <CardActions>
                    <Button size="small" color="primary" component={Link} to={"/jobs/" + job.id + "?edit=true"}>
                        Edit
                    </Button>
                </CardActions>
            </Card>
        )
    }

    render() {
        if (this.state.redirectTo) {
            return (
                <Redirect push to={"/jobs/" + this.state.clicked} />
            )
        } else {
            return (
                <DocumentTitle title="Josh's Dashboard - Jobs">
                    <Paper style={{ padding: 10 }}>
                        <Typography variant="h5" component="h2">
                            Jobs
                        </Typography>
                        <Divider variant="middle" style={{ marginTop: 10, marginBottom: 10 }} />
                        <Typography variant="h5" component="h3">
                            Active
                        </Typography>
                        <Grid container spacing={24}>
                            {this.state.activeJobs.map((job, index) => {
                                return (
                                    <Grid item xs={6}>
                                        {this.renderCard(job)}
                                    </Grid>
                                )
                            })}
                            {this.state.activeJobs.length <= 0 && <Typography style={{ margin: 20 }} variant="body1" component="p">
                                No Active Jobs
                        </Typography>}
                        </Grid>
                        <Divider variant="middle" style={{ marginTop: 10, marginBottom: 10 }} />
                        <Typography variant="h5" component="h3">
                            Inactive
                        </Typography>
                        <Grid container spacing={24}>
                            {this.state.inactiveJobs.map((job, index) => {
                                return (
                                    <Grid item xs={6}>
                                        {this.renderCard(job)}
                                    </Grid>
                                )
                            })}
                            {this.state.inactiveJobs.length <= 0 && <Typography style={{ margin: 20 }} variant="body1" component="p">
                                No Inactive Jobs
                        </Typography>}
                        </Grid>
                    </Paper>
                </DocumentTitle>
            )
        }

    }
}

export default Jobs;