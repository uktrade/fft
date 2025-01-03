/**
 *
 * @param {object} props
 * @param {types.PayrollData[]} props.payroll
 * @returns
 */
export default function PayrollTable({
  headers,
  payroll,
  onTogglePayPeriods,
  RowComponent,
}) {
  if (payroll.length === 0) {
    return <p className="govuk-body">No data found</p>;
  }
  return (
    <>
      <div className="scrollable">
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
                  key={row.id}
                  row={row}
                  onTogglePayPeriods={onTogglePayPeriods}
                />
              );
            })}
          </tbody>
        </table>
      </div>
    </>
  );
}
