import { getScriptJsonData, postData } from "../../Util";

import * as types from "./types";

/**
 * Fetch payroll data and return it as a promise.
 *
 * @returns {Promise<types.PayrollData[]>} A promise resolving to an array of objects containing employee information.
 */
export function getPayrollData() {
  return getScriptJsonData("payroll-data");
}

/**
 * Post modified payroll data.
 *
 * @param {types.PayrollData[]} payroll - Payroll data to be sent.
 * @returns {import("../../Util").PostDataResponse} - Updated payroll data received.
 */
export function postPayrollData(payroll) {
  const response = postData("", payroll);
  console.log("response", response);
  return response;
}
