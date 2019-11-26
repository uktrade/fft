import React from 'react';
import { Provider } from 'react-redux';
import { store } from './Store';
//import { PersistGate } from 'redux-persist/integration/react';
import ForecastTable from './Components/ForecastTable/index'

function App() {
    return (
        <Provider store={store}>
            <ForecastTable />
        </Provider>
    );
}

export default App;
