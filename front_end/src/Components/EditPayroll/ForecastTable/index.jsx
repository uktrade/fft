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
                    {{ month }}
                  </th>
                );
              })}
            </tr>
          </thead>
          <tbody className="govuk-table__body">
            {forecast.map((row) => {
              return (
                <tr className="govuk-table__row" key={row.natural_account_code}>
                  <th scope="row" className="govuk-table__header">
                    {row.programme_code}
                  </th>
                  <th scope="row" className="govuk-table__header">
                    {row.natural_account_code}
                  </th>
                  <td className="govuk-table__cell">£{row.apr}</td>
                  <td className="govuk-table__cell">£{row.may}</td>
                  <td className="govuk-table__cell">£{row.jun}</td>
                  <td className="govuk-table__cell">£{row.jul}</td>
                  <td className="govuk-table__cell">£{row.aug}</td>
                  <td className="govuk-table__cell">£{row.sep}</td>
                  <td className="govuk-table__cell">£{row.oct}</td>
                  <td className="govuk-table__cell">£{row.nov}</td>
                  <td className="govuk-table__cell">£{row.dec}</td>
                  <td className="govuk-table__cell">£{row.jan}</td>
                  <td className="govuk-table__cell">£{row.feb}</td>
                  <td className="govuk-table__cell">£{row.mar}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </>
  );
}
