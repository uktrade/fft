import React from 'react'
import ReactDOM from 'react-dom'
import Forecast from './Apps/Forecast'
import CostCentre from './Apps/CostCentre'
import * as serviceWorker from './serviceWorker'

if (document.getElementById('forecast-app')) {
	ReactDOM.render(<Forecast />, document.getElementById('forecast-app'))
} else if (document.getElementById('cost-centre-list-app')) {
	ReactDOM.render(<CostCentre />, document.getElementById('cost-centre-list-app'))
}





// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
