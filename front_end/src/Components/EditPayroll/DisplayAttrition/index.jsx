import PayModifierHeaders from "../PayModifierHeaders";
import DisplayPayModifier from "../DisplayPayModifier";

const percentageToDecimal = (percentage) => {
  return 1.0 - percentage / 100;
};

const decimalToPercentage = (decimal) => {
  // Rounded to prevent decimal precision issues
  return Math.round((1.0 - decimal) * 100 * 1e10) / 1e10;
};

const DisplayAttrition = ({
  attrition = [],
  global_attrition = [],
  onInputChange,
  onCreate,
}) => {
  if (attrition.length > 0) {
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
                    <div class="govuk-input__wrapper">
                      <input
                        className="govuk-input govuk-input--width-5"
                        id={`modifier-${index}`}
                        name={`modifier-${index}`}
                        type="number"
                        defaultValue={decimalToPercentage(value)}
                        onChange={(e) =>
                          onInputChange(
                            index,
                            percentageToDecimal(e.target.value),
                          )
                        }
                      ></input>
                      <div class="govuk-input__suffix" aria-hidden="true">
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
