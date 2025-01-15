/**
 * @typedef {Object} EmployeeData
 * @property {string} name - The employee's name.
 * @property {string} grade - The employee's grade.
 * @property {string} employee_no - The employee's number.
 * @property {number} fte - The employee's FTE.
 * @property {string} programme_code - The employee's programme code.
 * @property {string} budget_type - The employee's programme code budget type.
 * @property {string} assignment_status - The employee's assignment status.
 * @property {string} basic_pay - The employee's basic pay.
 * @property {boolean[]} pay_periods - Whether the employee is being paid in periods.
 */

/**
 * @typedef {Object} VacancyData
 * @property {string} id - The vacancy's pk.
 * @property {string} grade - The vacancy's grade.
 * @property {string} programme_code - The vacancy's programme code.
 * @property {string} budget_type - The vacancy's programme code budget type.
 * @property {string} recruitment_type - The vacancy's recruitment type.
 * @property {string} recruitment_stage - The vacancy's recruitment stage.
 * @property {string} appointee_name - The vacancy's appointee name.
 * @property {string} hiring_manager - The vacancy's hiring manager.
 * @property {string} hr_ref - The vacancy's hr ref.
 * @property {boolean[]} pay_periods - Whether the vacancy is being paid in periods.
 */

/**
 * @typedef {Object} PayModifierData
 * @property {number} id - The pay modifier's pk.
 * @property {number[]} pay_modifiers - The pay modifier's monthly percentages
 */

/**
 * @typedef {Object} PreviousMonthsData
 * @property {string} month_short_name - The short form name of the month
 * @property {int} month_financial_code - The financial index of the month (Apr is 1 etc)
 */

/**
 * @typedef {Object} ForecastData
 * @property {string} programme_code - The forecast data's programme code
 * @property {string} natural_account_code - The forecast data's natural account code
 * @property {int} apr - The forecast data in pence for april
 * @property {int} may - The forecast data in pence for may
 * @property {int} jun - The forecast data in pence for june
 * @property {int} jul - The forecast data in pence for july
 * @property {int} aug - The forecast data in pence for august
 * @property {int} sep - The forecast data in pence for september
 * @property {int} oct - The forecast data in pence for october
 * @property {int} nov - The forecast data in pence for november
 * @property {int} dec - The forecast data in pence for december
 * @property {int} jan - The forecast data in pence for january
 * @property {int} feb - The forecast data in pence for february
 * @property {int} mar - The forecast data in pence for march
 */
/**
 * @typedef {Object} PayrollData
 * @property {EmployeeData[]} employees - A list of employees
 * @property {VacancyData[]} vacancies - A list of vacancies
 * @property {PayModifierData[]} pay_modifiers - A list of pay modifiers
 * @property {ForecastData[]} forecast - A list of forecast data
 * @property {PreviousMonthsData[]} previous_months - A list of months with actuals loaded
 */

export const Types = {};
