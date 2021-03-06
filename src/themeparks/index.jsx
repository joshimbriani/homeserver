import React from 'react';
import { BrowserRouter as Router, Route, withRouter } from "react-router-dom";
import DocumentTitle from 'react-document-title';

import CoasterHome from './home.jsx';
import CoasterGoals from './goals.jsx';
import CoasterGoalsNew from './goalsNew.jsx';
import CoasterGoalsSpec from './goalsSpec.jsx';
import CoasterJournals from './journals.jsx';
import CoasterJournalsNew from './journalsNew.jsx';
import CoasterJournalsSpec from './journalsSpec.jsx';

class CoasterIndex extends React.Component {
    render() {
        return (
            <DocumentTitle title="Josh's Dashboard - Theme Parks - ">
                <div>
                    <Route exact path={`${this.props.match.url}/`} component={() => <CoasterHome />} />
                    <Route exact path={`${this.props.match.url}/goals`} component={() => <CoasterGoals />} />
                    <Route exact path={`${this.props.match.url}/goals/new`} component={() => <CoasterGoalsNew />} />
                    <Route path={`${this.props.match.url}/goals/:goalid([0-9]+)`} component={() => <CoasterGoalsSpec />} />
                    <Route exact path={`${this.props.match.url}/journals`} component={() => <CoasterJournals />} />
                    <Route exact path={`${this.props.match.url}/journals/new`} component={() => <CoasterJournalsNew />} />
                    <Route path={`${this.props.match.url}/journals/:journalid([0-9]+)`} component={() => <CoasterJournalsSpec />} />
                    <Route exact path={`${this.props.match.url}/parks/:parkid`} component={() => <CoasterHome />} />
                    <Route path={`${this.props.match.url}/parks/:parkid/:rideid`} component={() => <CoasterHome />} />
                </div>
                </DocumentTitle>
        )
    }
}

export default withRouter(CoasterIndex);