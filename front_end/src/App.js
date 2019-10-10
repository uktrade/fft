import React, {Fragment, useState, useEffect, useRef } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import { Provider } from 'react-redux';
import { store } from './Store';
import { PersistGate } from 'redux-persist/integration/react';
import ForecastTable from './Components/ForecastTable/index'

function App() {
    return (
        <Provider store={store}>
            <ForecastTable />
        </Provider>
    );
}

export default App;