import React from 'react';
import { Provider } from 'react-redux';
import { store } from './../Store';
import EditPayrollNonEmployee from './../Components/EditPayrollNonEmployee/index'

function PayrollNonEmployee() {
    return (
        <Provider store={store}>
            <EditPayrollNonEmployee />
        </Provider>
    );
}

export default PayrollNonEmployee;
