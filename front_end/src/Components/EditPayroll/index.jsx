import * as types from "./types";

/**
 *
 * @param {object} props
 * @param {types.EmployeeData[]} props.payroll
 * @returns
 */
export default function EditPayoll({ payroll, onLogPayroll }) {
  return (
    <>
      <h1>Edit payroll</h1>
      <button onClick={onLogPayroll}>Log payroll</button>
      {payroll.map((row) => {
        return <p>{row.name}</p>;
      })}
    </>
  );
}
