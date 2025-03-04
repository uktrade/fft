import NotesCell from "../../Notes/NotesCell";
import PayPeriods from "../PayPeriods";

const EmployeeRow = ({
  row,
  onTogglePayPeriods,
  previousMonths,
  showPreviousMonths,
}) => {
  return (
    <tr className="govuk-table__row">
      <td className="govuk-table__cell">{row.name}</td>
      <td className="govuk-table__cell">{row.grade}</td>
      <td className="govuk-table__cell">{row.employee_no}</td>
      <td className="govuk-table__cell">{row.fte}</td>
      <td className="govuk-table__cell">{row.programme_code}</td>
      <td className="govuk-table__cell">{row.budget_type}</td>
      <td className="govuk-table__cell">{row.assignment_status}</td>
      <PayPeriods
        row={row}
        id={row.id}
        onTogglePayPeriods={onTogglePayPeriods}
        previousMonths={previousMonths}
        showPreviousMonths={showPreviousMonths}
      />
      <td className="govuk-table__cell">
        <NotesCell notes={row.notes} employee_no={row.employee_no} />
      </td>
    </tr>
  );
};

export default EmployeeRow;
