import { formatMoney } from "../../../Util";

export default function ForecastTable({ forecast, months }) {
  return (
    <>
      <h2 className="govuk-heading-m">Payroll forecast</h2>

      <div className="scrollable">
        <table className="govuk-table">
          <thead className="govuk-table__head">
            <tr className="govuk-table__row">
              <th scope="col" className="govuk-table__header">
                Programme code
              </th>
              <th scope="col" className="govuk-table__header">
                Natural account code
              </th>
              {months.map((month) => {
                return (
                  <th scope="col" className="govuk-table__header" key={month}>
                    {month}
                  </th>
                );
              })}
            </tr>
          </thead>
          <tbody className="govuk-table__body">
            {forecast.map((row, index) => {
              return (
                <tr className="govuk-table__row" key={index}>
                  <th scope="row" className="govuk-table__header">
                    {row.programme_code}
                  </th>
                  <th scope="row" className="govuk-table__header">
                    {row.natural_account_code}
                  </th>
                  {months.map((month) => (
                    <td className="govuk-table__cell" key={month}>
                      £{formatMoney(row[month.toLowerCase()])}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </>
  );
}
