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
 * @returns {import("../../Util").PostDataResponse} Updated payroll data received.
 */
export function postPayrollData(payrollData) {
  return postData(getPayrollApiUrl(), JSON.stringify(payrollData));
}

/**
 * Fetch vacancy data and return it as a promise.
 * @returns {Promise<types.VacancyData[]>} A promise resolving to an array of objects containing vacancy information.
 */
export function getVacancyData() {
  return getData(getPayrollApiUrl() + "vacancies/").then((data) => data.data);
}

/**
 * Post modified vacancy data.
 *
 * @param {types.VacancyData[]} vacancyData - Vacancy data to be sent.
 * @returns {import("../../Util").PostDataResponse} Updated vacancy data received.
 */
export function postVacancyData(vacancyData) {
  return postData(
    getPayrollApiUrl() + "vacancies/",
    JSON.stringify(vacancyData),
  );
}

/**
 * Fetch pay modifier data and return it as a promise.
 * @returns {Promise<types.PayModifierData[]>} A promise resolving to an array of objects containing pay modifier information.
 */
export function getPayModifierData() {
  return getData(getPayrollApiUrl() + "pay_modifiers/").then(
    (data) => data.data,
  );
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
