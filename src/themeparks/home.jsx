import React from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import { Grid, Paper } from '@material-ui/core';
import DocumentTitle from 'react-document-title';

import ScreamscapeCard from './components/screamscapecard.jsx';
import ArticlesCard from './components/articlescard.jsx';
import ParkCard from './components/parkcard.jsx';
import GoalCard from './components/goalscard.jsx';

class CoasterHome extends React.Component {
    render() {
        return (
            <DocumentTitle title="Josh's Dashboard - Theme Parks - Home">
            <Grid container spacing={16}>
                <Grid item xs={4}>
                    <ScreamscapeCard />
                    <GoalCard />
                    <ArticlesCard />
                </Grid>
                <Grid item xs={8}>
                    <ParkCard park={"IOA"} />
                    <ParkCard park={"USF"} style={{ marginTop: 20, paddingTop: 20 }} />
                    <ParkCard park={"USJ"} style={{ marginTop: 20 }} />
                    <ParkCard park={"USH"} style={{ marginTop: 20 }} />
                    <ParkCard park={"CP"} style={{ marginTop: 20 }} />
                    <ParkCard park={"CGA"} style={{ marginTop: 20 }} />
                </Grid>
            </Grid>
            </DocumentTitle>
        )
    }
}

export default CoasterHome;