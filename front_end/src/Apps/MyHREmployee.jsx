import React from 'react';
import { Provider } from 'react-redux';
import { store } from './../Store';
import MyHREmployee from "../Components/MyHREmployee/index.jsx";

function GroupMyHREmployee() {
    return (
        <Provider store={store}>
            <MyHREmployee />
        </Provider>
    );
}

export default GroupMyHREmployee;
