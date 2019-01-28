import React from 'react';
import ReactDOM from 'react-dom';
import { MuiPickersUtilsProvider } from 'material-ui-pickers';
import MomentUtils from '@date-io/moment';

import AppRouter from './approuter.jsx'; 

class App extends React.Component {
    render() {
        return (
            <MuiPickersUtilsProvider utils={MomentUtils}>
                <AppRouter />
            </MuiPickersUtilsProvider>
            
        );
    }
}

ReactDOM.render(<App />, document.getElementById('app'));