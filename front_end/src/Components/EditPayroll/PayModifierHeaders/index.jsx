import { monthsToTitleCase } from "../../../Util";

const PayModifierHeaders = () => {
  return (
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
  );
};

export default PayModifierHeaders;
