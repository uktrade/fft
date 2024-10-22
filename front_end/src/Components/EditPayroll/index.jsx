import * as types from "./types";
import PayrollTable from "./PayrollTable/index";

/**
 *
 * @param {object} props
 * @param {types.PayrollData[]} props.payroll
 * @returns
 */
export default function EditPayroll({
  payroll,
  onSavePayroll,
  onTogglePayPeriods,
}) {
  const headers = [
    "Name",
    "Employee No",
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
    <>
      <PayrollTable
        headers={headers}
        payroll={payroll}
        onTogglePayPeriods={onTogglePayPeriods}
      ></PayrollTable>
      <button className="govuk-button" onClick={onSavePayroll}>
        Save payroll
      </button>
    </>
  );
}
