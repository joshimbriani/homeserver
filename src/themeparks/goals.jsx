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

class Goals extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            activeGoals: [],
            abandonedGoals: [],
            completedGoals: [],
            clicked: -1,
            redirectTo: false
        }
    }

    componentDidMount() {
        this.setState({ loading: true })
        fetch(URL + "api/v1/coastergoals/")
            .then(response => response.json())
            .then(responseJSON => {
                var active = [];
                var abandoned = [];
                var completed = [];

                for (var i = 0; i < responseJSON.length; i++) {
                    if (responseJSON[i]["status"] === 1) {
                        active.push(responseJSON[i]);
                    } else if (responseJSON[i]["status"] === 2) {
                        abandoned.push(responseJSON);
                    } else {
                        completed.push(responseJSON);
                    }
                }

                this.setState({ activeGoals: active, abandonedGoals: abandoned, completedGoals: completed, loading: false })
            })
    }

    renderCard(goal) {
        return (
            <Card style={styles.card}>
                <CardActionArea onClick={() => this.setState({ clicked: goal.id, redirectTo: true })}>
                    <CardMedia
                        component="img"
                        alt={goal.title}
                        style={styles.media}
                        height="140"
                        image={"/static/uploads/themeparks/goals/" + goal.id + ".jpeg"}
                        title={goal.title}
                    />
                    <CardContent>
                        <Typography gutterBottom variant="h5" component="h2">
                            {goal.title}
                        </Typography>
                        <Typography component="p">
                            {goal.description}
                        </Typography>
                        <div style={{ marginTop: 10 }}>
                            <Line percent={goal.progress} strokeWidth="4" strokeColor="#2196F3" />
                        </div>
                    </CardContent>
                </CardActionArea>
                <CardActions>
                    <Button size="small" color="primary" component={Link} to={"/themeparks/goals/" + goal.id}>
                        Edit
                                    </Button>
                    <Button size="small" color="primary" component={Link} to={"/themeparks/goals/new/"}>
                        Add a Goal
                                    </Button>
                </CardActions>
            </Card>
        )
    }

    render() {
        if (this.state.redirectTo) {
            return (
                <Redirect push to={"/themeparks/goals/" + this.state.clicked} />
            )
        } else {
            return (
                <DocumentTitle title="Josh's Dashboard - Theme Parks - Goals">
                    <Paper style={{ padding: 10 }}>
                        <Typography variant="h5" component="h2">
                            Goals
                    </Typography>
                        <Divider variant="middle" style={{ marginTop: 10, marginBottom: 10 }} />
                        <Typography variant="h5" component="h3">
                            Active
                    </Typography>
                        <Grid container spacing={24}>
                            {this.state.activeGoals.map((goal, index) => {
                                return (
                                    <Grid item xs={6}>
                                        {this.renderCard(goal)}
                                    </Grid>
                                )
                            })}
                            {this.state.activeGoals.length <= 0 && <Typography style={{ margin: 20 }} variant="body1" component="p">
                                No Active Goals
                        </Typography>}
                        </Grid>
                        <Divider variant="middle" style={{ marginTop: 10, marginBottom: 10 }} />
                        <Typography variant="h5" component="h3">
                            Abandoned
                    </Typography>
                        <Grid container spacing={24}>
                            {this.state.abandonedGoals.map((goal, index) => {
                                return (
                                    <Grid item xs={6}>
                                        {this.renderCard(goal)}
                                    </Grid>
                                )
                            })}
                            {this.state.abandonedGoals.length <= 0 && <Typography style={{ margin: 20 }} variant="body1" component="p">
                                No Abandoned Goals
                        </Typography>}
                        </Grid>
                        <Divider variant="middle" style={{ marginTop: 10, marginBottom: 10 }} />
                        <Typography variant="h5" component="h3">
                            Completed
                    </Typography>
                        <Grid container spacing={24}>
                            {this.state.completedGoals.map((goal, index) => {
                                return (
                                    <Grid item xs={6}>
                                        {this.renderCard(goal)}
                                    </Grid>
                                )
                            })}
                            {this.state.completedGoals.length <= 0 && <Typography style={{ margin: 20 }} variant="body1" component="p">
                                No Completed Goals
                        </Typography>}
                        </Grid>
                    </Paper>
                </DocumentTitle>
            )
        }

    }
}

export default Goals;