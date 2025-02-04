import PayModifierHeaders from "../PayModifierHeaders";

const DisplayPayModifier = ({ data }) => {
  if (data.length === 0) {
    return (
      <>
        <h3 className="govuk-heading-s">Pay uplift</h3>
        <p className="govuk-body">No pay uplift set</p>
      </>
    );
  }

  return data.map((row, index) => (
    <div className="govuk-form-group" key={index}>
      <h3 className="govuk-heading-s">{row.name}</h3>
      <table className="govuk-table">
        <PayModifierHeaders />
        <tbody className="govuk-table__body">
          <tr className="govuk-table__row">
            {row.pay_modifiers.map((value, index) => {
              return (
                <td className="govuk-table__cell" key={index}>
                  {value}
                </td>
              );
            })}
          </tr>
        </tbody>
      </table>
    </div>
  ));
};

export default DisplayPayModifier;
