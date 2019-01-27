import React from 'react';
import ReactDOM from 'react-dom';

import AppRouter from './approuter.jsx'; 

class App extends React.Component {
    render() {
        return (
            <AppRouter />
        );
    }
}

ReactDOM.render(<App />, document.getElementById('app'));