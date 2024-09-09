import 'vite/modulepreload-polyfill'
import React from 'react'
import ReactDOM from 'react-dom'
import Forecast from './Apps/Forecast'
import CostCentre from './Apps/CostCentre'
import * as serviceWorker from './serviceWorker'
import CostCentrePayroll from "./Apps/CostCentrePayroll.jsx";
import PayrollEmployee from "./Apps/PayrollEmployee.jsx";
import PayrollNonEmployee from "./Apps/PayrollNonEmployee.jsx";

if (document.getElementById('forecast-app')) {
	ReactDOM.render(<Forecast />, document.getElementById('forecast-app'))
} else if (document.getElementById('cost-centre-list-app')) {
	ReactDOM.render(<CostCentre />, document.getElementById('cost-centre-list-app'))
} else if (document.getElementById('cost-centre-payroll-list-app')) {
	ReactDOM.render(<CostCentrePayroll />, document.getElementById('cost-centre-payroll-list-app'))
}

if (document.getElementById('payroll-employee-app')) {
	ReactDOM.render(<PayrollEmployee />, document.getElementById('payroll-employee-app'))
}

if (document.getElementById('payroll-non-employee-app')) {
	ReactDOM.render(<PayrollNonEmployee />, document.getElementById('payroll-non-employee-app'))
}

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
