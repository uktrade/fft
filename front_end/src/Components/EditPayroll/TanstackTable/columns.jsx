import { monthsToTitleCase } from "../../../Util";
import NotesCell from "../../Notes/NotesCell";
import { totalOfColumn } from "./helpers";

// Specific column getters
function getMonthsColumns(data, onTogglePayPeriods, previousMonths) {
  return monthsToTitleCase.map((header, index) => ({
    header: header,
    footer: totalOfColumn(data, (data) =>
      data.pay_periods[index] === true ? 1 : 0,
    ),
    id: header.toLowerCase(),
    enableSorting: false,
    accessorFn: (row) => row.pay_periods[index],
    cell: ({ getValue, row }) => (
      <input
        type="checkbox"
        checked={getValue()}
        disabled={previousMonths[index].is_actual}
        onChange={() => onTogglePayPeriods(row.original.id, index, getValue())}
      />
    ),
    meta: {
      className: "payroll-checkbox",
    },
  }));
}

function getNotesColumn(section) {
  return {
    header: "Notes",
    enableSorting: false,
    cell: ({ row }) => (
      <NotesCell
        section={section}
        notes={row.original.notes}
        id={row.original.id}
      />
    ),
  };
}

const GRADE_COLUMN = {
  accessorKey: "grade",
  header: "Grade",
  filterFn: "fuzzy",
};

const PROGRAMME_CODE_COLUMN = {
  accessorKey: "programme_code",
  header: "Programme code",
};

const BUDGET_TYPE_COLUMN = {
  accessorKey: "budget_type",
  header: "Budget type",
};

// Table column getters

export default function getPayrollColumns(
  data,
  onTogglePayPeriods,
  previousMonths,
) {
  const monthColumns = getMonthsColumns(
    data,
    onTogglePayPeriods,
    previousMonths,
  );
  const employeeColumns = [
    {
      accessorKey: "name",
      header: "Name",
      footer: `${data.length} rows`,
      filterFn: "fuzzy",
    },
    GRADE_COLUMN,
    {
      accessorKey: "employee_no",
      header: "Employee no",
    },
    {
      accessorKey: "fte",
      header: "FTE",
      footer: totalOfColumn(data, (data) => data.fte),
      sortDescFirst: false,
    },
    PROGRAMME_CODE_COLUMN,
    BUDGET_TYPE_COLUMN,
    {
      accessorKey: "assignment_status",
      header: "Assignment status",
    },
  ];
  const notesColumn = getNotesColumn("employees");

  return [...employeeColumns, ...monthColumns, notesColumn];
}

export function getVacanciesColumns(data, onTogglePayPeriods, previousMonths) {
  const monthColumns = getMonthsColumns(
    data,
    onTogglePayPeriods,
    previousMonths,
  );
  const vacancyColumns = [
    {
      header: "Manage",
      footer: `${data.length} rows`,
      cell: ({ row }) => (
        <a
          className="govuk-button govuk-button--secondary govuk-!-margin-0"
          href={`vacancies/${row.original.id}/edit`}
        >
          Edit
        </a>
      ),
    },
    {
      accessorKey: "recruitment_type",
      header: "Recruitment type",
    },
    GRADE_COLUMN,
    PROGRAMME_CODE_COLUMN,
    BUDGET_TYPE_COLUMN,
    {
      accessorKey: "appointee_name",
      header: "Appointee name",
      filterFn: "fuzzy",
    },
    {
      accessorKey: "hiring_manager",
      header: "Hiring manager",
      filterFn: "fuzzy",
    },
    {
      accessorKey: "hr_ref",
      header: "HR ref",
    },
    {
      accessorKey: "recruitment_stage",
      header: "Recruitment stage",
    },
  ];
  const notesColumn = getNotesColumn("vacancies");

  return [...vacancyColumns, ...monthColumns, notesColumn];
}
