import { getData, postData } from "../../Util";

import * as types from "./types";

/**
 * Fetch payroll data and return it as a promise.
 * @returns {Promise<types.PayrollData[]>} A promise resolving to an array of objects containing employee information.
 */
export function getPayrollData() {
  return getData(getPayrollApiUrl()).then((data) => data.data);
}

/**
 * Post modified payroll data.
 *
 * @param {types.PayrollData[]} payrollData - Payroll data to be sent.
 * @returns {import("../../Util").PostDataResponse} - Updated payroll data receieved.
 */
export function postPayrollData(payrollData) {
  return postData(getPayrollApiUrl(), payrollData);
}

function getPayrollApiUrl() {
  const costCentreCode = window.costCentreCode;
  const financialYear = window.financialYear;
  return `/payroll/api/${costCentreCode}/${financialYear}/`;
}
