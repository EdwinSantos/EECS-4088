import React, { Component } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import UsernamePicker from './UsernamePicker';
import Room from './Room/Room';
import Double07 from './Games/Double07';
import HotPotato from './Games/Hot_Potato';
import Match from './Games/Match';
import Fragments from './Games/Fragments';
import MultiGame from './Games/MultiGame';
import NotFound from './NotFound';
import io from 'socket.io-client';

class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            username: '',
            socket: '',
            gameList: []
        };
        // Initialize socket
        this.socket = io();
    }

    updateUsername = (username) => {
        this.setState({ username: username });
        // Store username in a session storage
        sessionStorage.setItem('username', username);
    };
    updateSocketId = (socketId) => {
        this.setState({ socketId: socketId });
        // Store socketId in a session storage
        sessionStorage.setItem('socketId', socketId);
    };
    updateGameList = (gameList) => {
        this.setState({ gameList: gameList });
        // Store game list in session storage
        sessionStorage.setItem('gameList', gameList);
    };

    render() {
        return (
            <BrowserRouter>
                <Switch>
                    <Route
                        exact
                        path="/"
                        render={(props) => <UsernamePicker {...props}
                        userState={this.state}
                        socket={this.socket}
                        updateUsername={this.updateUsername}
                        updateSocketId={this.updateSocketId}
                        updateGameList={this.updateGameList}
                        />} 
                    />
                    <Route
                        path="/room"
                        render={(props) => <Room {...props}
                        userState={this.state}
                        socket={this.socket}
                        />}
                    />
                    <Route
                        path="/Double07" 
                        render={(props) => <Double07 {...props}
                        userState={this.state}
                        socket={this.socket}
                        />}
                    />
                    <Route
                        path="/Hot_Potato"
                        render={(props) => <HotPotato {...props}
                        userState={this.state}
                        socket={this.socket}
                        />}
                    />
                    <Route
                        path="/Match"
                        render={(props) => <Match {...props}
                        userState={this.state}
                        socket={this.socket}
                        />}
                    />
                    <Route
                        path="/Fragments"
                        render={(props) => <Fragments {...props}
                        userState={this.state}
                        socket={this.socket}
                        />}
                    />
                    <Route
                        path="/MultiGame"
                        render={(props) => <MultiGame {...props}
                        userState={this.state}
                        socket={this.socket}
                        />}
                    />
                    <Route path="/" component={NotFound} />
                </Switch>
            </BrowserRouter>
        );
    }
}

export default App;