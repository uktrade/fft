import EmployeeRow from "../EmployeeRow";

/**
 *
 * @param {object} props
 * @param {types.PayrollData[]} props.payroll
 * @returns
 */
export default function PayrollTable({ headers, payroll, onTogglePayPeriods, RowComponent }) {
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
          {payroll.map((row) => {
            return (
              <RowComponent
                row={row}
                onTogglePayPeriods={onTogglePayPeriods}
              />
            );
          })}
        </tbody>
      </table>
    </>
  );
}
