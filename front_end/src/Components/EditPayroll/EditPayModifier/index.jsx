const EditPayModifier = ({ obj }) => {
  const headers = monthsTitle;
  return (
    <table className="govuk-table">
      <thead className="govuk-table__head">
        <tr className="govuk-table__row">
          {headers.map((header) => {
            return (
              <th scope="col" className="govuk-table__header" key={header}>
                {header}
              </th>
            );
          })}
        </tr>
      </thead>
      <tbody className="govuk-table__body"></tbody>
    </table>
  );
};

export default EditPayModifier;
