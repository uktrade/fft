import { getData, postData } from "../../Util";

import * as types from "./types";

const vacanciesSlug = "vacancies/";
const payModifiersSlug = "pay_modifiers/";
const previousMonthsSlug = "previous_months/";

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
  return getData(getPayrollApiUrl() + vacanciesSlug).then((data) => data.data);
}

/**
 * Post modified vacancy data.
 *
 * @param {types.VacancyData[]} vacancyData - Vacancy data to be sent.
 * @returns {import("../../Util").PostDataResponse} Updated vacancy data received.
 */
export function postVacancyData(vacancyData) {
  return postData(
    getPayrollApiUrl() + vacanciesSlug,
    JSON.stringify(vacancyData),
  );
}

/**
 * Fetch pay modifier data and return it as a promise.
 * @returns {Promise<types.PayModifierData[]>} A promise resolving to an array of objects containing pay modifier information.
 */
export function getPayModifierData() {
  return getData(getPayrollApiUrl() + payModifiersSlug).then(
    (data) => data.data,
  );
}

/**
 * Post modified pay modifiers data.
 *
 * @param {types.PayModifierData[]} payModifierData - Pay modifier data to be sent.
 * @returns {import("../../Util").PostDataResponse} Updated pay modifier data received.
 */
export function postPayModifierData(payModifierData) {
  return postData(
    getPayrollApiUrl() + payModifiersSlug,
    JSON.stringify(payModifierData),
  );
}

/**
 * Fetch previous months data and return it as a promise.
 * @returns {Promise<types.PreviousMonthsData[]>} A promise resolving to an array of objects containing previous months information.
 */
export function getPreviousMonthsData() {
  return getData(getPayrollApiUrl() + previousMonthsSlug).then(
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
