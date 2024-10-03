import React from 'react';
import { Provider } from 'react-redux';
import { store } from './../Store';
import EditPayrollEmployee from './../Components/EditPayrollEmployee/index'

function PayrollEmployee() {
    return (
        <Provider store={store}>
            <EditPayrollEmployee />
        </Provider>
    );
}

export default PayrollEmployee;
