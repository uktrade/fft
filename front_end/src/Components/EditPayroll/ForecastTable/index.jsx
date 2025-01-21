import { formatMoney } from "../../../Util";

export default function ForecastTable({
  forecast,
  actuals,
  months,
  previousMonths,
}) {
  function getMatchingActual(programme_code, natural_account_code) {
    const matchingGroup = actuals.find(
      (group) => group.programme_code === programme_code,
    );
    let matchingItems = [];
    if (matchingGroup) {
      const matchingCode = matchingGroup.data.find(
        (n) => n.natural_account_code == natural_account_code,
      );
      matchingItems = matchingCode ? matchingCode.items : [];
    }
    return matchingItems;
  }

  const getClass = (index) => {
    return previousMonths[index] && previousMonths[index].is_actual
      ? "not-editable"
      : "";
  };

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
              const actual = getMatchingActual(
                row.programme_code,
                row.natural_account_code,
              );

              return (
                <tr className="govuk-table__row" key={index}>
                  <th scope="row" className="govuk-table__header">
                    {row.programme_code}
                  </th>
                  <th scope="row" className="govuk-table__header">
                    {row.natural_account_code}
                  </th>
                  {months.map((month, index) => {
                    let amount = row[month.toLowerCase()];
                    if (actual && previousMonths[index].is_actual) {
                      amount = actual[index].amount;
                    }

                    return (
                      <td
                        className={`govuk-table__cell ${getClass(index)}`}
                        key={month}
                      >
                        £{formatMoney(amount)}
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
