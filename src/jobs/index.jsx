import React from 'react';
import { BrowserRouter as Router, Route, withRouter } from "react-router-dom";
import DocumentTitle from 'react-document-title';

import Jobs from './jobs.jsx';
import JobsNew from './jobsNew.jsx';
import JobsSpec from './jobsSpec.jsx'

class JobsIndex extends React.Component {
    render() {
        return (
            <DocumentTitle title="Josh's Dashboard - Jobs - ">
                <div>
                    <Route exact path={`${this.props.match.url}/`} component={() => <Jobs />} />
                    <Route path={`${this.props.match.url}/:jobid([0-9]+)`} component={() => <JobsSpec />} />
                    <Route exact path={`${this.props.match.url}/new`} component={() => <JobsNew />} />
                </div>
            </DocumentTitle>
        )
    }
}

export default withRouter(JobsIndex);