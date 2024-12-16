import { monthsToTitleCase } from "../../../Util";

const EditPayModifier = ({ data, onInputChange }) => {
  return (
    data.length > 0 && (
      <div className="govuk-form-group">
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
                    <input
                      className="govuk-input"
                      id={`modifier-${index}`}
                      name={`modifier-${index}`}
                      type="number"
                      defaultValue={value}
                      onChange={(e) =>
                        onInputChange(data[0].id, index, e.target.value)
                      }
                    ></input>
                  </td>
                );
              })}
            </tr>
          </tbody>
        </table>
      </div>
    )
  );
};

export default EditPayModifier;
