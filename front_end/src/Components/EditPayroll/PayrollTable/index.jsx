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
}) {
  const previousMonthsOffset = previousMonths.length;
  if (payroll.length === 0) {
    return <p className="govuk-body">No data found</p>;
  }
  return (
    <>
      <div className="scrollable">
        <table className="govuk-table">
          <thead className="govuk-table__head">
            <tr className="govuk-table__row">
              {headers
                .filter(
                  (header) =>
                    !previousMonths.some(
                      (month) => month.month_short_name === header,
                    ),
                )
                .map((header) => {
                  return (
                    <th
                      scope="col"
                      className="govuk-table__header"
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
              const filteredPayPeriods =
                row.pay_periods.slice(previousMonthsOffset);
              const updatedRow = { ...row, pay_periods: filteredPayPeriods };
              return (
                <RowComponent
                  key={row.id}
                  row={updatedRow}
                  onTogglePayPeriods={onTogglePayPeriods}
                  previousMonthsOffset={previousMonthsOffset}
                />
              );
            })}
          </tbody>
        </table>
      </div>
    </>
  );
}
