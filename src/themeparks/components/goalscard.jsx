import React from 'react';
import { Grid, Paper, Typography, Card, CardMedia, CardContent, CardActionArea, CardActions, Button } from '@material-ui/core';
import Carousel from '../../reusable/carousel.jsx';
import { Link, Redirect } from "react-router-dom";
import { URL } from '../../utils/network';
import ArrowForwardIcon from '@material-ui/icons/ArrowForward';
import ArrowBackIcon from '@material-ui/icons/ArrowBack';
import { Line } from 'rc-progress';

const styles = {
    card: {
        maxWidth: 345,
    },
    media: {
        // ⚠️ object-fit is not supported by IE 11.
        objectFit: 'cover',
    },
};

class GoalsCard extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            goals: [],
            loading: false,
            showIndex: 0,
            clicked: -1,
            redirectTo: false
        }

        this.timer = this.timer.bind(this);
    }

    componentDidMount() {
        this.setState({ loading: true });
        fetch(URL + "api/v1/coastergoals?status=1&limit=5")
            .then(response => response.json())
            .then(responseJSON => this.setState({ goals: responseJSON, loading: false }));

        var intervalId = setInterval(this.timer, 10000);
        this.setState({ intervalId: intervalId });
    }

    componentWillUnmount() {
        // use intervalId from the state to clear the interval
        clearInterval(this.state.intervalId);
    }

    timer() {
        // setState method is used to update the state
        this.setState({ showIndex: (this.state.showIndex + 1) >= this.state.goals.length ? 0 : (this.state.showIndex + 1) });
    }

    render() {
        if (this.state.redirectTo) {
            return (
                <Redirect push to={"/themeparks/goals/" + this.state.clicked} />
            )
        } else {
            return (
                <Paper style={{ marginTop: 20 }}>
                    <Typography
                        component="h2"
                        variant="h5"
                        color="inherit"
                        align="center"
                        noWrap
                    >
                        Goals
                </Typography>
                    {this.state.goals.length === 0 && <div>
                        <Typography
                            component="h4"
                            variant="h5"
                            color="inherit"
                            align="center"
                            noWrap
                        >
                            No Goals
                </Typography>
                    </div>}
                    <Grid container spacing={24}>
                        <Grid item xs={12} sm={6} style={{ textAlign: 'center' }}>
                            <ArrowBackIcon onClick={() => {
                                const max = this.state.goals.length;
                                this.setState({ showIndex: (this.state.showIndex - 1) < 0 ? (max - 1) : (this.state.showIndex - 1) });
                                console.log(max, this.state.showIndex)
                            }} />
                        </Grid>
                        <Grid item xs={12} sm={6} style={{ textAlign: 'center' }}>
                            <ArrowForwardIcon onClick={() => {
                                const max = this.state.goals.length;
                                this.setState({ showIndex: (this.state.showIndex + 1) >= max ? 0 : (this.state.showIndex + 1) });
                            }} />
                        </Grid>
                    </Grid>
                    <Carousel showIndex={this.state.showIndex}>
                        {this.state.goals.map((goal) => {
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
                        })}
                    </Carousel>
                </Paper>
            )
        }
    }
}

export default GoalsCard;