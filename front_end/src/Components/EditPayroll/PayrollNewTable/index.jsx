import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  getSortedRowModel,
} from "@tanstack/react-table";
import { monthsToTitleCase } from "../../../Util";
import { useState } from "react";
import { monthsWithActuals } from "./helpers";

function PayrollNewTable({ data, onTogglePayPeriods, previousMonths }) {
  const monthColumns = monthsToTitleCase.map((header, index) => ({
    header: header,
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
  // State
  const columns = [...employeeColumns, ...monthColumns];
  const [sorting, setSorting] = useState([]);
  const [showPreviousMonths, setShowPreviousMonths] = useState(false);

  // Table state
  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
    },
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    onSortingChange: setSorting,
  });

  // Handlers
  const togglePreviousMonthsVisibility = () => {
    setShowPreviousMonths((prev) => !prev);
    const monthColumnIds = monthsWithActuals(previousMonths);
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
          type="checkbox"
          checked={showPreviousMonths}
          onChange={togglePreviousMonthsVisibility}
        />
        Hide previous months
      </label>
      <table>
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th
                  colSpan={header.colSpan}
                  key={header.id}
                  onClick={header.column.getToggleSortingHandler()}
                  style={{
                    cursor: header.column.getCanSort() ? "pointer" : "default",
                  }}
                >
                  {header.isPlaceholder
                    ? null
                    : flexRender(
                        header.column.columnDef.header,
                        header.getContext(),
                      )}
                  {{
                    asc: " ▲",
                    desc: " ▼",
                    false: header.column.getCanSort() ? " ⬍" : null,
                  }[header.column.getIsSorted()] ?? null}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <td
                  key={cell.id}
                  className={cell.column.columnDef.meta?.className ?? ""}
                >
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
