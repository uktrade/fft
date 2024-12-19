import { monthsToTitleCase } from "../../../Util";

const EditPayModifier = ({ data, onInputChange }) => {
  if (data.length === 0) {
    return <p className="govuk-body">No modifiers set</p>;
  }
  return data.map((row, index) => (
    <div className="govuk-form-group" key={index}>
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
            {row.pay_modifiers.map((value, index) => {
              return (
                <td className="govuk-table__cell" key={index}>
                  <input
                    className="govuk-input"
                    id={`modifier-${index}`}
                    name={`modifier-${index}`}
                    type="number"
                    defaultValue={value}
                    onChange={(e) =>
                      onInputChange(row.id, index, e.target.value)
                    }
                  ></input>
                </td>
              );
            })}
          </tr>
        </tbody>
      </table>
    </div>
  ));
};

export default EditPayModifier;
