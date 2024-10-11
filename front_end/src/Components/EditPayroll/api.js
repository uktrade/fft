import { getScriptJsonData } from "../../Util";

import * as types from "./types";

/**
 * Fetch employee data and return it as a promise.
 *
 * @returns {Promise<types.EmployeeData[]>} A promise resolving to an array of objects containing employee information.
 */
export function getPayrollData() {
  return getScriptJsonData("payroll-data");
}
