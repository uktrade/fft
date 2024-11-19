import * as types from "./types";
import PayrollTable from "./PayrollTable/index";

/**
 *
 * @param {object} props
 * @param {types.PayrollData[]} props.payroll
 * @returns
 */
export default function EditPayroll({ payroll, onTogglePayPeriods }) {
  const headers = [
    "Name",
    "Grade",
    "Employee No",
    "FTE",
    "Programme Code",
    "Budget Type",
    "Assignment Status",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
    "Jan",
    "Feb",
    "Mar",
  ];
  return (
    <PayrollTable
      headers={headers}
      payroll={payroll}
      onTogglePayPeriods={onTogglePayPeriods}
    ></PayrollTable>
  );
}
