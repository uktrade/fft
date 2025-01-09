/**
 * @typedef {Object} PayrollData
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

export const Types = {};
