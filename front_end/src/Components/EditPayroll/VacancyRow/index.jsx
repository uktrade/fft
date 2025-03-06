import NotesCell from "../../Notes/NotesCell";
import PayPeriods from "../PayPeriods";

const VacancyRow = ({
  row,
  onTogglePayPeriods,
  previousMonths,
  showPreviousMonths,
}) => {
  return (
    <tr className="govuk-table__row">
      <td className="govuk-table__header">
        <a
          className="govuk-button govuk-button--secondary govuk-!-margin-0"
          href={`vacancies/${row.id}/edit`}
        >
          Edit
        </a>
      </td>
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
        previousMonths={previousMonths}
        showPreviousMonths={showPreviousMonths}
      />
      <td className="govuk-table__cell">
        <NotesCell section="vacancies" notes={row.notes} id={row.id} />
      </td>
    </tr>
  );
};

export default VacancyRow;
