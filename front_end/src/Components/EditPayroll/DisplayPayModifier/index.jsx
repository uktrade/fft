import { valueAboveOneToPercentage } from "../../../Util";
import PayModifierHeaders from "../PayModifierHeaders";

const DisplayPayModifier = ({ modifier = [], title }) => {
  if (modifier.length === 0) {
    return (
      <>
        <h3 className="govuk-heading-s">{title}</h3>
        <p className="govuk-body">No {title.toLowerCase()} set</p>
      </>
    );
  }

  return (
    <>
      <h3 className="govuk-heading-s">{title}</h3>
      <table className="govuk-table">
        <PayModifierHeaders />
        <tbody className="govuk-table__body">
          <tr className="govuk-table__row">
            {modifier.map((value, index) => {
              return (
                <td className="govuk-table__cell" key={index}>
                  {valueAboveOneToPercentage(value)}%
                </td>
              );
            })}
          </tr>
        </tbody>
      </table>
    </>
  );
};

export default DisplayPayModifier;
