import React from 'react';
import { BrowserRouter as Router, Route, withRouter } from "react-router-dom";

import CoasterHome from './home.jsx';

class CoasterIndex extends React.Component {
    render() {
        return (
            <Router>
                <div>
                    <Route exact path={`${this.props.match.url}/`} component={() => <CoasterHome />} />
                    <Route exact path={`${this.props.match.url}/goals/`} component={() => <CoasterHome />} />
                    <Route path={`${this.props.match.url}/goals/:goalid`} component={() => <CoasterHome />} />
                    <Route exact path={`${this.props.match.url}/parks/:parkid/`} component={() => <CoasterHome />} />
                    <Route path={`${this.props.match.url}/parks/:parkid/:rideid`} component={() => <CoasterHome />} />
                </div>
            </Router>
        )
    }
}

export default withRouter(CoasterIndex);