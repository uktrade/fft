import PayModifierHeaders from "../PayModifierHeaders";

const DisplayPayModifier = ({
  data,
  title,
  isAttrition = false,
  onCreate = [],
}) => {
  if (!data || data <= 0) {
    return (
      <>
        <h3 className="govuk-heading-s">{title}</h3>
        <p className="govuk-body">No {title.toLowerCase()} set</p>
        {isAttrition && (
          <button
            className="govuk-button govuk-button--secondary"
            onClick={onCreate}
          >
            Add Attrition
          </button>
        )}
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
            {data.map((value, index) => {
              return (
                <td className="govuk-table__cell" key={index}>
                  {value}
                </td>
              );
            })}
          </tr>
        </tbody>
      </table>
      {isAttrition && (
        <>
          <p className="govuk-body">
            This attrition is for the current financial year. You can add one
            for this specific cost centre instead.
          </p>
          <button
            className="govuk-button govuk-button--secondary"
            onClick={onCreate}
          >
            Add Attrition
          </button>
        </>
      )}
    </>
  );
};

export default DisplayPayModifier;
