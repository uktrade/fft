import * as types from "./types";
import PayrollTable from "./PayrollTable/index";

/**
 *
 * @param {object} props
 * @param {types.PayrollData[]} props.payroll
 * @returns
 */
export default function EditPayroll({ payroll, headers, onTogglePayPeriods }) {
  return (
    <PayrollTable
      headers={headers}
      payroll={payroll}
      onTogglePayPeriods={onTogglePayPeriods}
    ></PayrollTable>
  );
}
