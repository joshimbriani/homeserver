import React from 'react';
import { Redirect } from "react-router-dom";
import { Grid, Paper, Typography, TextField, Button } from '@material-ui/core';
import { URL } from '../utils/network';
import DocumentTitle from 'react-document-title';

class JobsNew extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            name: '',
            description: '',
            progress: 0,
            success: false,
            redirectID: null
        }

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit() {
        if (this.state.name && this.state.description) {
            const data = new FormData();
            data.append('picture', this.uploadInput.files[0]);
            data.append('title', this.state.name);
            data.append("description", this.state.description);
            data.append('progress', this.state.progress);
            data.append('status', 1);

            fetch(URL + 'api/v1/coastergoals/', {
                method: 'POST',
                body: data
            }).then(response => response.json())
                .then(responseJSON => {
                    if (responseJSON["success"] && responseJSON["id"]) {
                        this.setState({ success: true, redirectID: responseJSON["id"] })
                    }
                })
        }
    }

    render() {
        if (this.state.success) {
            return (
                <Redirect to={"/themeparks/goals/" + this.state.redirectID} />
            )
        } else {
            return (
                <DocumentTitle title="Josh's Dashboard - Theme Parks - New Goal">
                    <Paper style={{ padding: 10 }}>
                        <Typography variant="h5" component="h2">
                            Create a New Goal
                    </Typography>
                        <Grid container spacing={24}>
                            <Grid item xs={12}>
                                <TextField
                                    id="goal-name"
                                    label="Name"
                                    value={this.state.name}
                                    fullWidth
                                    onChange={(event) => this.setState({ name: event.target.value })}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    id="goal-progress"
                                    label="Progress"
                                    value={this.state.progress}
                                    type="number"
                                    fullWidth
                                    onChange={(event) => this.setState({ progress: event.target.value })}
                                />
                            </Grid>
                            <Grid item xs={12}>
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
                            </Grid>
                            <Grid item xs={12}>
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
                            </Grid>
                            <Grid item xs={12}>
                                <Button variant="contained" color="primary" onClick={this.handleSubmit}>
                                    Submit
                        </Button>
                            </Grid>
                        </Grid>
                    </Paper>
                </DocumentTitle>
            )
        }
    }
}

export default JobsNew;