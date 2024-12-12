import { monthsToTitleCase } from "../../../Util";

const EditPayModifier = ({ pay_modifier }) => {
  return (
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
      <tbody className="govuk-table__body"></tbody>
    </table>
  );
};

export default EditPayModifier;
