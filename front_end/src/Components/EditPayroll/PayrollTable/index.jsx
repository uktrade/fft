import EmployeeRow from "../EmployeeRow";

/**
 *
 * @param {object} props
 * @param {types.PayrollData[]} props.payrollData
 * @returns
 */
export default function PayrollTable({
  headers,
  payrollData,
  onTogglePayPeriods,
}) {
  return (
    <>
      <table className="govuk-table">
        <thead className="govuk-table__head">
          <tr className="govuk-table__row">
            {headers.map((header) => {
              return (
                <th scope="col" className="govuk-table__header" key={header}>
                  {header}
                </th>
              );
            })}
          </tr>
        </thead>
        <tbody className="govuk-table__body">
          {payrollData.map((row) => {
            return (
              <EmployeeRow
                row={row}
                key={row.employee_no}
                onTogglePayPeriods={onTogglePayPeriods}
              />
            );
          })}
        </tbody>
      </table>
    </>
  );
}
