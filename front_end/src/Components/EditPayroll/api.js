import { getData, postJsonData } from "../../Util";

import * as types from "./types";

/**
 * Fetch payroll data and return it as a promise.
 * @returns {Promise<types.PayrollData[]>} A promise resolving to an array of objects containing payroll information.
 */
export async function getPayrollData() {
  const [employees, data] = await Promise.all([
    _get("employees"),
    getData(getPayrollApiUrl()),
  ]);

  return {
    employees,
    ...data,
  };
}

/**
 * Post modified payroll data.
 *
 * @param {types.PayrollData[]} payrollData - Payroll data to be sent.
 * @returns {import("../../Util").PostDataResponse} Updated payroll data received.
 */
export function postPayrollData(payrollData) {
  return postJsonData(getPayrollApiUrl(), payrollData);
}

/**
 * Create default pay modifier object
 */
export function createPayModifiers() {
  return postJsonData(getPayrollApiUrl() + "pay_modifiers/");
}

function _get(resource) {
  return getData(`/api/payroll/${resource}/`, {
    cost_centre_code: window.costCentreCode,
    financial_year: window.financialYear,
  });
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
