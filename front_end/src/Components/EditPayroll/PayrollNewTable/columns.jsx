import { monthsToTitleCase } from "../../../Util";
import { totalOfColumn } from "./helpers";

export default function getPayrollColumns(data, previousMonths) {
  const monthColumns = monthsToTitleCase.map((header, index) => ({
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
  const employeeColumns = [
    {
      accessorKey: "name",
      header: "Name",
      footer: `${data.length} rows`,
      filterFn: "fuzzy",
    },
    {
      accessorKey: "grade",
      header: "Grade",
      filterFn: "fuzzy",
    },
    {
      accessorKey: "employee_no",
      header: "Employee No",
      filterFn: "fuzzy",
    },
    {
      accessorKey: "fte",
      header: "FTE",
      footer: totalOfColumn(data, (data) => data.fte),
      sortDescFirst: false,
    },
    {
      accessorKey: "programme_code",
      header: "Programme Code",
    },
    {
      accessorKey: "budget_type",
      header: "Budget Type",
    },
    {
      accessorKey: "assignment_status",
      header: "Assignment Status",
    },
  ];

  return [...employeeColumns, ...monthColumns];
}
