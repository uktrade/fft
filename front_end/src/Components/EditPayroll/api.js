import { getData, postData } from "../../Util";

import * as types from "./types";

/**
 * Fetch payroll data and return it as a promise.
 * @returns {Promise<types.PayrollData[]>} A promise resolving to an array of objects containing payroll information.
 */
export function getPayrollData() {
  return getData(getPayrollApiUrl());
}

/**
 * Post modified payroll data.
 *
 * @param {types.PayrollData[]} payrollData - Payroll data to be sent.
 * @returns {import("../../Util").PostDataResponse} Updated payroll data received.
 */
export function postPayrollData(payrollData) {
  return postData(getPayrollApiUrl(), JSON.stringify(payrollData));
}

/**
 * Return the payroll API URL.
 *
 * This function relies on the `costCentreCode` and `financialYear` being available on
 * the `window` object.
 *
 * @returns {string} The payroll API URL.
 */
function getPayrollApiUrl() {
  const costCentreCode = window.costCentreCode;
  const financialYear = window.financialYear;
  return `/payroll/api/${costCentreCode}/${financialYear}/`;
}
