import PayPeriods from "../PayPeriods";

const VacancyRow = ({ row, onTogglePayPeriods }) => {
  return (
    <tr className="govuk-table__row">
      <td className="govuk-table__cell">{row.recruitment_type}</td>
      <td className="govuk-table__cell">{row.grade}</td>
      <td className="govuk-table__cell">{row.programme_code}</td>
      <td className="govuk-table__cell">{row.budget_type}</td>
      <td className="govuk-table__cell">{row.appointee_name}</td>
      <td className="govuk-table__cell">{row.hiring_manager}</td>
      <td className="govuk-table__cell">{row.hr_ref}</td>
      <td className="govuk-table__cell">{row.recruitment_stage}</td>
      <PayPeriods
        row={row}
        id={row.id}
        onTogglePayPeriods={onTogglePayPeriods}
      />
    </tr>
  );
};

export default VacancyRow;
