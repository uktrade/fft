import * as types from "./types";
import PayrollTable from "../../Components/PayrollTable/index";

/**
 *
 * @param {object} props
 * @param {types.PayrollData[]} props.payroll
 * @returns
 */
export default function EditPayroll({ payroll, onLogPayroll }) {
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
      <h1>Edit payroll</h1>
      {/* <button onClick={onLogPayroll}>Log payroll</button> */}
      <PayrollTable headers={headers} payrollData={payroll}></PayrollTable>
    </>
  );
}
