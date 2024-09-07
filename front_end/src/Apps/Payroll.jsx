import React from 'react';
import { Provider } from 'react-redux';
import { store } from './../Store';
import EditPayroll from './../Components/EditPayroll/index'

function Payroll() {
    return (
        <Provider store={store}>
            <EditPayroll />
        </Provider>
    );
}

export default Payroll;
