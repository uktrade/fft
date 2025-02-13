import PayModifierHeaders from "../PayModifierHeaders";
import DisplayPayModifier from "../DisplayPayModifier";

const DisplayAttrition = ({
  attrition,
  global_attrition,
  onInputChange,
  onCreate,
}) => {
  if (attrition && attrition.length > 0) {
    return (
      <div className="govuk-form-group">
        <h3 className="govuk-heading-s">Attrition</h3>
        <table className="govuk-table">
          <PayModifierHeaders />
          <tbody className="govuk-table__body">
            <tr className="govuk-table__row">
              {attrition.map((value, index) => {
                return (
                  <td className="govuk-table__cell" key={index}>
                    <input
                      className="govuk-input"
                      id={`modifier-${index}`}
                      name={`modifier-${index}`}
                      type="number"
                      defaultValue={value}
                      onChange={(e) => onInputChange(index, e.target.value)}
                    ></input>
                  </td>
                );
              })}
            </tr>
          </tbody>
        </table>
      </div>
    );
  }

  if (global_attrition && global_attrition.length > 0) {
    return (
      <>
        <DisplayPayModifier data={global_attrition} title="Global attrition" />
        <p className="govuk-body">
          This attrition is for the current financial year. You can add one for
          this specific cost centre instead.
        </p>
        <button
          className="govuk-button govuk-button--secondary"
          onClick={onCreate}
        >
          Add Attrition
        </button>
      </>
    );
  }

  return (
    <>
      <h3 className="govuk-heading-s">Attrition</h3>
      <p className="govuk-body">No attrition set</p>
      <button
        className="govuk-button govuk-button--secondary"
        onClick={onCreate}
      >
        Add Attrition
      </button>
    </>
  );
};

export default DisplayAttrition;
