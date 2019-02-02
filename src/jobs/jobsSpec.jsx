import React from 'react';
import { Redirect } from "react-router-dom";
import { Fab, Paper, Typography, TextField, Button, Card, CardActionArea, CardMedia, CardContent, CardActions, FormControl, InputLabel, MenuItem, Dialog, DialogActions, DialogTitle, DialogContent, DialogContentText } from '@material-ui/core';
import { URL } from '../utils/network';
import EditIcon from '@material-ui/icons/Edit';
import { withRouter } from "react-router-dom";
import DeleteForeverIcon from '@material-ui/icons/DeleteForever';
import DocumentTitle from 'react-document-title';
import Select from 'react-select';

const styles = {
    media: {
        // ⚠️ object-fit is not supported by IE 11.
        objectFit: 'cover',
    },
};

class JobsSpec extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            name: '',
            description: '',
            cronString: '',
            pythonFile: '',
            active: { value: true, label: 'Active' },
            editing: false,
            job: {},
            loading: false,
            open: false,
            redirect: false
        }

        this.handleEdit = this.handleEdit.bind(this);
    }

    componentDidMount() {
        this.setState({ loading: true })
        fetch(URL + "api/v1/jobs/" + this.props.match.params.jobid)
            .then(response => response.json())
            .then(responseJSON => this.setState({ job: responseJSON, loading: false, editing: false, name: responseJSON["name"], description: responseJSON["description"], pythonFile: responseJSON["pythonFile"], cronString: responseJSON["cronString"], active: {value: responseJSON["active"], label: responseJSON["active"] ? "Active" : "Inactive "} }))
    }

    handleEdit() {
        if (this.state.name && this.state.description && this.state.cronString && this.state.pythonFile) {
            const data = new FormData();
            if (this.state.name !== this.state.job.name) {
                data.append('name', this.state.name);
            }
            if (this.state.description !== this.state.job.description) {
                data.append("description", this.state.description);
            }
            if (this.state.cronString !== this.state.job.cronString) {
                data.append('cronString', this.state.cronString);
            }
            if (this.state.pythonFile !== this.state.job.pythonFile) {
                data.append('pythonFile', this.state.pythonFile);
            }
            if (this.state.active !== this.state.job.active) {
                data.append('active', this.state.active.value)
            }

            fetch(URL + 'api/v1/jobs/' + this.props.match.params.jobid, {
                method: 'PUT',
                body: data
            }).then(response => response.json())
                .then(responseJSON => {
                    if (responseJSON["success"] && responseJSON["job"]) {
                        this.setState({ editing: false, job: responseJSON["job"] })
                    }
                })
        }
    }

    deleteGoal() {
        fetch(URL + 'api/v1/jobs/' + this.props.match.params.jobid, {
            method: 'DELETE',
        }).then(response => response.json())
            .then(responseJSON => {
                if (responseJSON["success"]) {
                    this.setState({ redirect: true })
                }
            })
    }

    render() {
        console.log(this.state)
        if (this.state.redirect) {
            return (
                <Redirect to={"/jobs"} />
            )
        }

        if (this.state.editing) {
            return (
                <DocumentTitle title="Josh's Dashboard - Jobs">
                    <div>
                        <Paper style={{ padding: 10 }}>
                            <Card style={styles.card}>
                                <CardContent>
                                    <TextField
                                        id="goal-name"
                                        label="Name"
                                        value={this.state.name}
                                        fullWidth
                                        onChange={(event) => this.setState({ name: event.target.value })}
                                    />
                                    <TextField
                                        id="goal-python-file"
                                        label="Python File Name"
                                        value={this.state.pythonFile}
                                        fullWidth
                                        onChange={(event) => this.setState({ pythonFile: event.target.value })}
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
                                        id="goal-cron-string"
                                        label="Cron String"
                                        value={this.state.cronString}
                                        fullWidth
                                        onChange={(event) => this.setState({ cronString: event.target.value })}
                                    />
                                    <Select
                                        value={this.state.active}
                                        options={[
                                            { value: false, label: 'Inactive' },
                                            { value: true, label: 'Active' }
                                        ]}
                                        onChange={(option) => this.setState({ active: option })}
                                    />
                                </CardContent>
                                <CardActions>
                                    <Button size="small" color="primary" onClick={() => this.setState({ editing: false, name: this.state.job.name, description: this.state.job.description, pythonFile: this.state.job.pythonFile, cronString: this.state.job.cronString, active: {value: this.state.job.active, label: this.state.job.active ? "Active" : "Inactive "} })}>
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
                            <DialogTitle id="alert-dialog-title">{"Are you sure you want to delete this job?"}</DialogTitle>
                            <DialogContent>
                                <DialogContentText id="alert-dialog-description">
                                    This does not delete the Python file itself. If you want that deleted, please delete it yourself.
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
                <DocumentTitle title="Josh's Dashboard - Jobs">
                    <Paper style={{ padding: 10 }}>
                        <Card style={styles.card}>
                            <CardContent>
                                <Typography variant="h6" color="textSecondary" component="p">
                                    Name
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

export default withRouter(JobsSpec);