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
  previousMonths,
  showPreviousMonths,
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
                const isActual = previousMonths.some(
                  (obj) => obj.month_short_name === header && obj.is_actual,
                );
                const isHidden =
                  showPreviousMonths && isActual ? " hidden" : "";
                return (
                  <th
                    scope="col"
                    className={`govuk-table__header ${isHidden}`}
                    key={header}
                  >
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
                  previousMonths={previousMonths}
                  showPreviousMonths={showPreviousMonths}
                />
              );
            })}
          </tbody>
        </table>
      </div>
    </>
  );
}
