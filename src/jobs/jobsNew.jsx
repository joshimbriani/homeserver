import React from 'react';
import { Redirect } from "react-router-dom";
import { Grid, Paper, Typography, TextField, Button } from '@material-ui/core';
import { URL } from '../utils/network';
import DocumentTitle from 'react-document-title';
import Select from 'react-select';

class JobsNew extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            name: '',
            description: '',
            cronString: '',
            pythonFile: '',
            active: { value: true, label: 'Active' },
            success: false,
            redirectID: null
        }

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit() {
        if (this.state.name && this.state.description && this.state.cronString && this.state.pythonFile) {
            const data = new FormData();
            data.append('name', this.state.name);
            data.append("description", this.state.description);
            data.append('cronString', this.state.cronString);
            data.append('pythonFile', this.state.pythonFile);
            data.append('active', this.state.active.value);

            fetch(URL + 'api/v1/jobs/', {
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
                <Redirect to={"/jobs/" + this.state.redirectID} />
            )
        } else {
            return (
                <DocumentTitle title="Josh's Dashboard - Jobs - New Job">
                    <Paper style={{ padding: 10 }}>
                        <Typography variant="h5" component="h2">
                            Create a New Job
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
                                    id="goal-python-file"
                                    label="Python File Name"
                                    value={this.state.pythonFile}
                                    fullWidth
                                    onChange={(event) => this.setState({ pythonFile: event.target.value })}
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
                                <TextField
                                    id="goal-cron-string"
                                    label="Cron String"
                                    value={this.state.cronString}
                                    fullWidth
                                    onChange={(event) => this.setState({ cronString: event.target.value })}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <Select
                                    value={this.state.active}
                                    options={[
                                        { value: false, label: 'Inactive' },
                                        { value: true, label: 'Active' }
                                    ]}
                                    onChange={(option) => this.setState({ active: option })}
                                />
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