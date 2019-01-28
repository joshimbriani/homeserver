import React from 'react';
import { Redirect } from "react-router-dom";
import { Fab, Paper, Typography, TextField, Button, Card, Divider, CardMedia, CardContent, CardActions, FormControl, InputLabel, Select, MenuItem } from '@material-ui/core';
import { URL } from '../utils/network';
import EditIcon from '@material-ui/icons/Edit';
import { withRouter } from "react-router-dom";
import moment from 'moment';
import Markdown from 'react-remarkable';
import AsyncSelect from 'react-select/lib/Async';
import { DatePicker } from 'material-ui-pickers';


const styles = {
    media: {
        // ⚠️ object-fit is not supported by IE 11.
        objectFit: 'cover',
    },
};

class JournalsSpec extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            title: '',
            content: '',
            datetime: moment(),
            park: {},
            editing: (new URLSearchParams(props.location.search)).get('edit') === "true" ? true : false,
            journal: {
                park: {
                    name: ""
                }
            },
            loading: false
        }

        this.handleEdit = this.handleEdit.bind(this);
    }

    componentDidMount() {
        this.setState({ loading: true })
        fetch(URL + "api/v1/coasters/journals/" + this.props.match.params.journalid)
            .then(response => response.json())
            .then(responseJSON => {
                this.setState({ journal: responseJSON, loading: false, title: responseJSON["title"], content: responseJSON["content"], datetime: moment(responseJSON["datetime"]) })
                var park = responseJSON["park"];

                park["value"] = responseJSON["park"]["id"]
                park["label"] = responseJSON["park"]["name"]
                this.setState({ park: park });
            })
    }

    handleEdit() {
        if (this.state.title && this.state.content && this.state.datetime) {
            const data = new FormData();
            if (this.uploadInput.files[0]) {
                data.append('picture', this.uploadInput.files[0]);
            }
            if (this.state.title !== this.state.journal.title) {
                data.append('title', this.state.title);
            }
            if (this.state.content !== this.state.journal.content) {
                data.append("content", this.state.content);
            }
            if (this.state.park.id !== this.state.journal.park.id) {
                data.append("park", this.state.park.id)
            }
            if (this.state.datetime !== this.state.journal.datetime) {
                data.append("datetime", moment(this.state.datetime).toISOString());
            }

            fetch(URL + 'api/v1/coasters/journals/' + this.props.match.params.journalid, {
                method: 'PUT',
                body: data
            }).then(response => response.json())
                .then(responseJSON => {
                    if (responseJSON["success"] && responseJSON["journal"]) {
                        this.setState({ editing: false, journal: responseJSON["journal"] })
                    }
                })
        }
    }

    cancelEdit() {
        this.setState({ editing: false, title: this.state.journal.title, content: this.state.journal.content, datetime: moment(this.state.journal.progress) })
        var park = this.state.journal.park;

        park["value"] = this.state.journal.park["id"]
        park["label"] = this.state.journal.park["name"]
        this.setState({ park: park });
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

        if (this.state.editing) {
            return (
                <Paper style={{ padding: 10 }}>
                    <Card style={styles.card}>
                        <CardMedia
                            component="img"
                            alt={this.state.title}
                            style={styles.media}
                            height="140"
                            image={"/static/uploads/journalEntry/" + this.state.journal.id + ".jpeg"}
                            title={this.state.title}
                        />
                        <CardContent>
                            <TextField
                                id="journal-title"
                                label="Name"
                                value={this.state.title}
                                fullWidth
                                onChange={(event) => this.setState({ title: event.target.value })}
                            />
                            <DatePicker 
                                value={this.state.datetime} 
                                onChange={(date) => this.setState({ datetime: date })} 
                            />
                            <TextField
                                id="goal-content"
                                label="Content"
                                multiline
                                rows="20"
                                value={this.state.content}
                                onChange={(event) => this.setState({ content: event.target.value })}
                                margin="normal"
                                fullWidth
                            />
                            <AsyncSelect
                                cacheOptions
                                loadOptions={promiseOptions}
                                defaultOptions
                                value={this.state.park}
                                onChange={(selectedOption) => this.setState({ park: selectedOption })}
                            />
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
                            <Button size="small" color="primary" onClick={() => this.cancelEdit()}>
                                Cancel
                                </Button>
                            <Button size="small" color="primary" onClick={() => this.handleEdit()}>
                                Save
                                </Button>
                        </CardActions>
                    </Card>
                </Paper>
            )
        } else {
            return (
                <Paper style={{ padding: 10 }}>
                    <Card style={styles.card}>
                        <CardMedia
                            component="img"
                            alt={this.state.title}
                            style={styles.media}
                            height="140"
                            image={"/static/uploads/journalEntry/" + (this.state.journal.id ? this.state.journal.id : "loading") + ".jpeg"}
                            title={this.state.title}
                        />
                        <CardContent>
                            <Typography variant="caption">
                                Title
                            </Typography>
                            <Typography variant="h2" paragraph>
                                {this.state.title}
                            </Typography>
                            <Typography variant="caption">
                                Date
                            </Typography>
                            <Typography variant="h6" component="p" paragraph>
                                {moment(this.state.datetime).format('dddd MMMM Do YYYY')}
                            </Typography>
                            <Typography variant="caption" >
                                Park
                            </Typography>
                            <Typography variant="h6" component="p" paragraph>
                                {this.state.journal.park.name}
                            </Typography>
                            <Divider variant="middle" style={{ marginTop: 10, marginBottom: 10 }} />
                            <Markdown>
                                {this.state.content}
                            </Markdown>
                        </CardContent>
                    </Card>
                    <Fab style={{ position: 'absolute', bottom: 20, right: 20 }} onClick={() => this.setState({ editing: true })}>
                        <EditIcon />
                    </Fab>
                </Paper>
            )
        }
    }
}

export default withRouter(JournalsSpec);