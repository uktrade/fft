import React, {Fragment, useState, useEffect, useRef } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import './App.css';
import { Provider } from 'react-redux';
import { store } from './Store';
import { PersistGate } from 'redux-persist/integration/react';
import Table from './Components/Table/index'

function App() {
    return (
        <Provider store={store}>
            <Table />
        </Provider>
    );
}

export default App;
