import PayModifierHeaders from "../PayModifierHeaders";

const EditPayModifier = ({ data, onInputChange, onCreate }) => {
  if (!data || data <= 0) {
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
  }

  return (
    <div className="govuk-form-group">
      <h3 className="govuk-heading-s">Attrition</h3>
      <table className="govuk-table">
        <PayModifierHeaders />
        <tbody className="govuk-table__body">
          <tr className="govuk-table__row">
            {data.map((value, index) => {
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
};

export default EditPayModifier;
