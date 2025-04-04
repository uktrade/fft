import { formatMoney } from "../../../Util";

export default function ForecastTable({ forecast, months }) {
  return (
    <>
      <h2 className="govuk-heading-m">Payroll forecast</h2>

      <p className="govuk-body">Save payroll changes to update this table.</p>

      <div className="scrollable">
        <table className="govuk-table">
          <thead className="govuk-table__head">
            <tr className="govuk-table__row">
              <th scope="col" className="govuk-table__header">
                Programme code
              </th>
              <th scope="col" className="govuk-table__header">
                Programme description
              </th>
              <th scope="col" className="govuk-table__header">
                <abbr title="Natural account code">NAC</abbr>
              </th>
              <th scope="col" className="govuk-table__header">
                <abbr title="Natural account code">NAC</abbr> description
              </th>
              {months.map((month) => {
                return (
                  <th
                    scope="col"
                    className="govuk-table__header"
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
                  <td>{row.programme_code}</td>
                  <td>{row.programme_description}</td>
                  <td>{row.natural_account_code}</td>
                  <td>{row.nac_description}</td>
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
