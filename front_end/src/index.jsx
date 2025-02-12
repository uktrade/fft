import "vite/modulepreload-polyfill";
import React from "react";
import ReactDOM from "react-dom/client";
import Forecast from "./Apps/Forecast";
import CostCentre from "./Apps/CostCentre";
import Payroll from "./Apps/Payroll";
import * as serviceWorker from "./serviceWorker";
import { getData, postData } from "./Util";

window.getData = getData;
window.postData = postData;
const forecast_app = document.getElementById("forecast-app");
const cost_centre_list_app = document.getElementById("cost-centre-list-app");
const payroll_app = document.getElementById("payroll-app");
const root = ReactDOM.createRoot(
  forecast_app || cost_centre_list_app || payroll_app,
);
if (forecast_app) {
  root.render(<Forecast />);
} else if (cost_centre_list_app) {
  root.render(<CostCentre />);
} else if (payroll_app) {
  root.render(<Payroll />);
}

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
