import { monthsToTitleCase } from "../../../Util";

const EditPayModifier = ({ data }) => {
  return (
    data.length > 0 && (
      <table className="govuk-table">
        <thead className="govuk-table__head">
          <tr className="govuk-table__row">
            {monthsToTitleCase.map((header) => {
              return (
                <th scope="col" className="govuk-table__header" key={header}>
                  {header}
                </th>
              );
            })}
          </tr>
        </thead>
        <tbody className="govuk-table__body">
          <tr className="govuk-table__row">
            {data[0].pay_modifiers.map((value, index) => {
              return (
                <td className="govuk-table__cell" key={index}>
                  {value}
                </td>
              );
            })}
          </tr>
        </tbody>
      </table>
    )
  );
};

export default EditPayModifier;
