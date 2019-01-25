import React from 'react';
import { Paper, Typography, Card, CardHeader, CardContent } from '@material-ui/core';
import Carousel from '../../reusable/carousel.jsx';
import { Link } from "react-router-dom";

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
            loading: false
        }
    }

    componentDidMount() {
        this.setState({ loading: true })
        fetch(URL + "api/v1/goals?status=active&limit=5")
            .then(response => response.json())
            .then(responseJSON => this.setState({ goals: responseJSON, loading: false }))
    }

    render() {
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
                <Carousel>
                    {this.state.goals.map((goal) => {
                        return (
                            <Card className={classes.card}>
                                <CardActionArea>
                                    <CardMedia
                                        component="img"
                                        alt={goal.title}
                                        className={classes.media}
                                        height="140"
                                        image="/static/images/cards/contemplative-reptile.jpg"
                                        title={goal.title}
                                    />
                                    <CardContent>
                                        <Typography gutterBottom variant="h5" component="h2">
                                            {goal.title}
                                        </Typography>
                                        <Typography component="p">
                                            {goal.description}
                                        </Typography>
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

export default GoalsCard;