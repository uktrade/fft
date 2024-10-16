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

                {Array.from({ length: 12 }, (period, index) => (
                  <td className="govuk-table__cell" key={period}>
                    <input
                      type="checkbox"
                      checked={row[`period_${index + 1}`]}
                      readOnly
                    />
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </table>
    </>
  );
}
