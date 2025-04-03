import PayModifierHeaders from "../PayModifierHeaders";
import DisplayPayModifier from "../DisplayPayModifier";

const DisplayAttrition = ({
  attrition = [],
  global_attrition = [],
  onInputChange,
  onCreate,
}) => {
  if (attrition.length > 0) {
    return (
      <div className="govuk-form-group">
        <Description />
        <table className="govuk-table">
          <PayModifierHeaders />
          <tbody className="govuk-table__body">
            <tr className="govuk-table__row">
              {attrition.map((value, index) => {
                return (
                  <td className="govuk-table__cell" key={index}>
                    <div class="govuk-input__wrapper">
                      <input
                        className="govuk-input govuk-input--width-3"
                        id={`modifier-${index}`}
                        name={`modifier-${index}`}
                        type="number"
                        defaultValue={value}
                        onChange={(e) => onInputChange(index, e.target.value)}
                      ></input>
                      <div className="govuk-input__suffix" aria-hidden="true">
                        %
                      </div>
                    </div>
                  </td>
                );
              })}
            </tr>
          </tbody>
        </table>
      </div>
    );
  }

  if (global_attrition.length > 0) {
    return (
      <>
        <Description />
        <DisplayPayModifier
          modifier={global_attrition}
          title="Global attrition"
        />
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
      <Description />
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

const Description = () => {
  return (
    <>
      <h3 className="govuk-heading-s">Attrition rate</h3>
      <p className="govuk-body">
        Attrition rate is the rate in which staff leave an organisation over a
        year. DBT sets a default rate of X% but you can override it for your
        cost centre.
      </p>
    </>
  );
};

export default DisplayAttrition;
