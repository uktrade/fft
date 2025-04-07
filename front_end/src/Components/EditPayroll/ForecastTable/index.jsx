import { formatMoney } from "../../../Util";

export default function ForecastTable({ forecast, months }) {
  const actualMonths = months.filter((month) => month.is_actual);
  const forecastMonths = months.filter((month) => !month.is_actual);

  return (
    <>
      <h2 className="govuk-heading-m">Payroll forecast</h2>

      <p className="govuk-body">Save payroll changes to update this table.</p>

      <div className="scrollable">
        <table className="govuk-table">
          <thead className="govuk-table__head">
            <tr>
              <th className="govuk-table__header" colSpan="2"></th>
              <th className="govuk-table__header" colSpan={actualMonths.length}>
                Actuals
              </th>
              <th
                className="govuk-table__header"
                colSpan={forecastMonths.length}
              >
                Forecast
              </th>
            </tr>
            <tr className="govuk-table__row">
              <th scope="col" className="govuk-table__header align-end">
                Programme code
              </th>
              <th scope="col" className="govuk-table__header align-end">
                Programme <br />
                description
              </th>
              <th scope="col" className="govuk-table__header align-end">
                <abbr title="Natural Account Code">NAC</abbr>
              </th>
              <th scope="col" className="govuk-table__header align-end">
                <abbr title="Natural Account Code">NAC</abbr> description
              </th>
              {months.map((month) => {
                return (
                  <th
                    scope="col"
                    className="govuk-table__header align-end"
                    key={month.key}
                  >
                    {month.short_name}
                  </th>
                );
              })}
            </tr>
          </thead>
          <tbody className="govuk-table__body">
            {forecast.map((row, index) => {
              return (
                <tr className="govuk-table__row" key={index}>
                  <td className="govuk-table__cell">{row.programme_code}</td>
                  <td className="govuk-table__cell">
                    {row.programme_description}
                  </td>
                  <td className="govuk-table__cell">
                    {row.natural_account_code}
                  </td>
                  <td className="govuk-table__cell">{row.nac_description}</td>
                  {months.map((month) => {
                    const isActualClass = month.is_actual ? "not-editable" : "";
                    return (
                      <td
                        className={`govuk-table__cell ${isActualClass}`}
                        key={month.key}
                      >
                        {formatMoney(row[month.key] ?? 0)}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </>
  );
}
