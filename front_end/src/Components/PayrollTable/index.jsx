export default function PayrollTable({ headers, payrollData }) {
  console.log(headers);
  console.log(payrollData);
  return (
    <>
      <table className="govuk-table">
        <thead className="govuk-table__head">
          <tr className="govuk-table__row">
            {headers.map((header, index) => {
              return (
                <th scope="col" className="govuk-table__header" key={header}>
                  {header}
                </th>
              );
            })}
          </tr>
        </thead>
        <tbody className="govuk-table__body">
          {payrollData.map((row, index) => {
            return (
              <tr className="govuk-table__row" key={row.employee_no}>
                <td className="govuk-table__cell">{row.name}</td>
                <td className="govuk-table__cell">{row.employee_no}</td>
                <td className="govuk-table__cell">
                  <input type="checkbox" checked={row.period_1} readOnly />
                </td>
                <td className="govuk-table__cell">
                  <input type="checkbox" checked={row.period_2} readOnly />
                </td>
                <td className="govuk-table__cell">
                  <input type="checkbox" checked={row.period_3} readOnly />
                </td>
                <td className="govuk-table__cell">
                  <input type="checkbox" checked={row.period_4} readOnly />
                </td>
                <td className="govuk-table__cell">
                  <input type="checkbox" checked={row.period_5} readOnly />
                </td>
                <td className="govuk-table__cell">
                  <input type="checkbox" checked={row.period_6} readOnly />
                </td>
                <td className="govuk-table__cell">
                  <input type="checkbox" checked={row.period_7} readOnly />
                </td>
                <td className="govuk-table__cell">
                  <input type="checkbox" checked={row.period_8} readOnly />
                </td>
                <td className="govuk-table__cell">
                  <input type="checkbox" checked={row.period_9} readOnly />
                </td>
                <td className="govuk-table__cell">
                  <input type="checkbox" checked={row.period_10} readOnly />
                </td>
                <td className="govuk-table__cell">
                  <input type="checkbox" checked={row.period_11} readOnly />
                </td>
                <td className="govuk-table__cell">
                  <input type="checkbox" checked={row.period_12} readOnly />
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </>
  );
}
