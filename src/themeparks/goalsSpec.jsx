import React from 'react';
import { Redirect } from "react-router-dom";
import { Fab, Paper, Typography, TextField, Button, Card, CardActionArea, CardMedia, CardContent, CardActions, FormControl, InputLabel, Select, MenuItem, Dialog, DialogActions, DialogTitle, DialogContent, DialogContentText } from '@material-ui/core';
import { URL } from '../utils/network';
import EditIcon from '@material-ui/icons/Edit';
import { Line } from 'rc-progress';
import { withRouter } from "react-router-dom";
import DeleteForeverIcon from '@material-ui/icons/DeleteForever';
import DocumentTitle from 'react-document-title';

const styles = {
    media: {
        // ⚠️ object-fit is not supported by IE 11.
        objectFit: 'cover',
    },
};

class GoalsSpec extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            name: '',
            description: '',
            progress: 0,
            editing: false,
            goal: {},
            status: 1,
            loading: false,
            open: false,
            redirect: false
        }

        this.handleEdit = this.handleEdit.bind(this);
    }

    componentDidMount() {
        this.setState({ loading: true })
        fetch(URL + "api/v1/coastergoals/" + this.props.match.params.goalid)
            .then(response => response.json())
            .then(responseJSON => this.setState({ goal: responseJSON, loading: false, name: responseJSON["title"], description: responseJSON["description"], progress: responseJSON["progress"], status: responseJSON["status"] }))
    }

    handleEdit() {
        if (this.state.name && this.state.description) {
            const data = new FormData();
            if (this.uploadInput.files[0]) {
                data.append('picture', this.uploadInput.files[0]);
            }
            if (this.state.name !== this.state.goal.title) {
                data.append('title', this.state.name);
            }
            if (this.state.description !== this.state.goal.description) {
                data.append("description", this.state.description);
            }
            if (this.state.progress !== this.state.goal.progress) {
                data.append('progress', this.state.progress);
            }
            if (this.state.status !== this.state.goal.status) {
                data.append('status', this.state.status);
            }

            fetch(URL + 'api/v1/coastergoals/' + this.props.match.params.goalid, {
                method: 'PUT',
                body: data
            }).then(response => response.json())
                .then(responseJSON => {
                    if (responseJSON["success"] && responseJSON["goal"]) {
                        this.setState({ editing: false, goal: responseJSON["goal"] })
                    }
                })
        }
    }

    deleteGoal() {
        fetch(URL + 'api/v1/coastergoals/' + this.props.match.params.goalid, {
            method: 'DELETE',
        }).then(response => response.json())
            .then(responseJSON => {
                if (responseJSON["success"]) {
                    this.setState({ redirect: true })
                }
            })
    }

    render() {
        if (this.state.redirect) {
            return (
                <Redirect to={"/themeparks/goals"} />
            )
        }

        if (this.state.editing) {
            return (
                <DocumentTitle title="Josh's Dashboard - Theme Parks - Goal">
                    <div>
                        <Paper style={{ padding: 10 }}>
                            <Card style={styles.card}>
                                <CardMedia
                                    component="img"
                                    alt={this.state.name}
                                    style={styles.media}
                                    height="140"
                                    image={"/static/uploads/themeparks/goals" + this.state.goal.id + ".jpeg"}
                                    title={this.state.name}
                                />
                                <CardContent>
                                    <TextField
                                        id="goal-name"
                                        label="Name"
                                        value={this.state.name}
                                        fullWidth
                                        onChange={(event) => this.setState({ name: event.target.value })}
                                    />
                                    <TextField
                                        id="goal-description"
                                        label="Description"
                                        multiline
                                        rows="4"
                                        value={this.state.description}
                                        onChange={(event) => this.setState({ description: event.target.value })}
                                        margin="normal"
                                        fullWidth
                                    />
                                    <TextField
                                        id="goal-progress"
                                        label="Progress"
                                        value={this.state.progress}
                                        type="number"
                                        fullWidth
                                        onChange={(event) => this.setState({ progress: event.target.value })}
                                    />
                                    <FormControl>
                                        <InputLabel htmlFor="age-simple">Status</InputLabel>
                                        <Select
                                            value={this.state.status}
                                            onChange={() => this.setState({ status: event.target.status })}
                                            inputProps={{
                                                name: 'status',
                                                id: 'status',
                                            }}
                                        >
                                            <MenuItem value={1}>Active</MenuItem>
                                            <MenuItem value={2}>Abandoned</MenuItem>
                                            <MenuItem value={3}>Completed</MenuItem>
                                        </Select>
                                    </FormControl>
                                </CardContent>
                                <CardActions>
                                    <Button
                                        variant="contained"
                                        component="label"
                                    >
                                        Upload Image
                                    <input
                                            ref={(ref) => { this.uploadInput = ref; }}
                                            type="file"
                                            name="picture"
                                            style={{ display: "none" }}
                                        />
                                    </Button>
                                    <Button size="small" color="primary" onClick={() => this.setState({ editing: false, title: this.state.goal.title, description: this.state.goal.description, progress: this.state.goal.progress })}>
                                        Cancel
                                </Button>
                                    <Button size="small" color="primary" onClick={() => this.handleEdit()}>
                                        Save
                                </Button>
                                </CardActions>
                            </Card>
                            <Fab style={{ position: 'absolute', bottom: 20, right: 20 }} onClick={() => this.setState({ open: true })}>
                                <DeleteForeverIcon />
                            </Fab>
                        </Paper>
                        <Dialog
                            open={this.state.open}
                            onClose={() => this.setState({ open: false })}
                            aria-labelledby="alert-dialog-title"
                            aria-describedby="alert-dialog-description"
                        >
                            <DialogTitle id="alert-dialog-title">{"Are you sure you want to delete this goal?"}</DialogTitle>
                            <DialogContent>
                                <DialogContentText id="alert-dialog-description">
                                    If you can't accomplish this, please mark this as abandoned. This is meant for mistake goals.
                            </DialogContentText>
                            </DialogContent>
                            <DialogActions>
                                <Button onClick={() => this.setState({ open: false })} color="primary" autoFocus>
                                    Nah
                    </Button>
                                <Button onClick={() => { this.deleteGoal(); this.setState({ open: false }) }} color="primary">
                                    Let's Do it!
                    </Button>
                            </DialogActions>
                        </Dialog>
                    </div>
                </DocumentTitle>
            )
        } else {
            return (
                <DocumentTitle title="Josh's Dashboard - Theme Parks - Goal">
                    <Paper style={{ padding: 10 }}>
                        <Card style={styles.card}>
                            <CardMedia
                                component="img"
                                alt={this.state.name}
                                style={styles.media}
                                height="140"
                                image={"/static/uploads/themeparks/goals/" + (this.state.goal.id ? this.state.goal.id : "loading") + ".jpeg"}
                                title={this.state.name}
                            />
                            <CardContent>
                                <Typography variant="h6" color="textSecondary" component="p">
                                    Title
                                </Typography>
                                <Typography variant="h5" component="h2" paragraph>
                                    {this.state.name}
                                </Typography>
                                <Typography variant="h6" color="textSecondary" component="p">
                                    Description
                                </Typography>
                                <Typography>
                                    {this.state.description}
                                </Typography>
                                <div style={{ marginTop: 10 }}>
                                    <Line percent={this.state.progress} strokeWidth="4" strokeColor="#2196F3" />
                                </div>
                            </CardContent>
                        </Card>
                        <Fab style={{ position: 'absolute', bottom: 20, right: 20 }} onClick={() => this.setState({ editing: true })}>
                            <EditIcon />
                        </Fab>
                    </Paper>
                </DocumentTitle>
            )
        }
    }
}

export default withRouter(GoalsSpec);