import { monthsToTitleCase } from "../../../Util";

const EditPayModifier = ({ data, onInputChange, onCreate }) => {
  if (data.length === 0) {
    return (
      <>
        <p className="govuk-body">No modifiers set</p>
        <button
          className="govuk-button govuk-button--secondary"
          onClick={onCreate}
        >
          Add Attrition
        </button>
      </>
    );
  }

  return data.map((row, index) => (
    <div className="govuk-form-group" key={index}>
      <h3 className="govuk-heading-s">Attrition</h3>
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
