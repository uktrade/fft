import {
  useReactTable,
  getCoreRowModel,
  flexRender,
} from "@tanstack/react-table";
import { monthsToTitleCase } from "../../../Util";
import { useState } from "react";

function PayrollNewTable({ data, onTogglePayPeriods, previousMonths }) {
  const monthsWithActuals = previousMonths
    .filter((month) => month.is_actual)
    .map((month) => month.short_name.toLowerCase());
  const monthColumns = monthsToTitleCase.map((header, index) => ({
    header: header,
    id: header.toLowerCase(),
    accessorFn: (row) => row.pay_periods[index],
    cell: ({ getValue, row }) => (
      <input
        type="checkbox"
        checked={getValue()}
        disabled={previousMonths[index].is_actual}
        onChange={() => onTogglePayPeriods(row.original.id, index, getValue())}
      />
    ),
  }));
  const employeeColumns = [
    {
      accessorKey: "name",
      header: "Name",
    },
    {
      accessorKey: "grade",
      header: "Grade",
    },
    {
      accessorKey: "employee_no",
      header: "Employee No",
    },
    {
      accessorKey: "fte",
      header: "FTE",
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
  const columns = [...employeeColumns, ...monthColumns];
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });
  const [showPreviousMonths, setShowPreviousMonths] = useState(false);
  const togglePreviousMonthsVisibility = () => {
    setShowPreviousMonths((prev) => !prev);
    const monthColumnIds = monthsWithActuals;
    monthColumnIds.forEach((columnId) => {
      const column = table.getColumn(columnId);
      if (column) {
        column.getIsVisible()
          ? column.toggleVisibility(false)
          : column.toggleVisibility(true);
      }
    });
  };

  return (
    <div className="new-table scrollable">
      <label>
        <input
          {...{
            type: "checkbox",
            checked: showPreviousMonths,
            onChange: togglePreviousMonthsVisibility,
          }}
        />{" "}
        Hide previous months
      </label>
      <table>
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th colSpan={header.colSpan} key={header.id}>
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext(),
                      )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default PayrollNewTable;
