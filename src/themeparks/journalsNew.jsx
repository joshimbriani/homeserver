import React from 'react';
import { Redirect } from "react-router-dom";
import { Grid, Paper, Typography, TextField, Button } from '@material-ui/core';
import { URL } from '../utils/network';
import moment from 'moment';
import AsyncSelect from 'react-select/lib/Async';
import { DatePicker } from 'material-ui-pickers';
import DocumentTitle from 'react-document-title';

class JournalsNew extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            name: '',
            content: '',
            datetime: moment(),
            park: -1,
            success: false,
            redirectID: null
        }

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit() {
        if (this.state.name && this.state.content && this.state.park !== -1) {
            const data = new FormData();
            data.append('picture', this.uploadInput.files[0]);
            data.append('title', this.state.name);
            data.append('content', this.state.content);
            data.append('datetime', moment(this.state.datetime).toISOString());
            data.append('park', this.state.park.id);

            fetch(URL + 'api/v1/coasters/journals/', {
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
        const promiseOptions = (inputValue, callback) => {
            fetch(URL + 'api/v1/coasters/parks?limit=5&nameContains=' + inputValue).then(response => response.json())
                .then(responseJSON => {
                    // For now, we'll mock out a response
                    var data = []
                    for (var i = 0; i < responseJSON.length; i++) {
                        data.push({ value: responseJSON[i].id, label: responseJSON[i].name, id: responseJSON[i].id })
                    }
                    callback(data)
                })
        }

        if (this.state.success) {
            return (
                <Redirect to={"/themeparks/journals/" + this.state.redirectID} />
            )
        } else {
            return (
                <DocumentTitle title="Josh's Dashboard - Theme Parks - New Journal">
                    <Paper style={{ padding: 10 }}>
                        <Typography variant="h5" component="h2">
                            Create a New Journal Entry
                    </Typography>
                        <Grid container spacing={24}>
                            <Grid item xs={12}>
                                <TextField
                                    id="journal-name"
                                    label="Title"
                                    value={this.state.name}
                                    fullWidth
                                    onChange={(event) => this.setState({ name: event.target.value })}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                    id="journal-content"
                                    label="Content"
                                    multiline
                                    rows="20"
                                    value={this.state.content}
                                    onChange={(event) => this.setState({ content: event.target.value })}
                                    margin="normal"
                                    fullWidth
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <DatePicker
                                    value={this.state.datetime}
                                    onChange={(date) => this.setState({ datetime: date })}
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <AsyncSelect
                                    cacheOptions
                                    loadOptions={promiseOptions}
                                    defaultOptions
                                    onChange={(selectedOption) => this.setState({ park: selectedOption })}
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

export default JournalsNew;