import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  getFilteredRowModel,
  getSortedRowModel,
} from "@tanstack/react-table";
import { monthsToTitleCase } from "../../../Util";
import { useState } from "react";
import { monthsWithActuals } from "./helpers";
import { rankItem } from "@tanstack/match-sorter-utils";

function PayrollNewTable({ data, onTogglePayPeriods, previousMonths }) {
  // Column helpers
  const fuzzyFilter = (row, columnId, value, addMeta) => {
    const itemRank = rankItem(row.getValue(columnId), value);
    addMeta({ itemRank });
    return itemRank.passed;
  };

  const totalOfColumn = (callback) => data.reduce((acc, cur) => acc + callback(cur), 0);

  // Columns
  const monthColumns = monthsToTitleCase.map((header, index) => ({
    header: header,
    footer: totalOfColumn((data) => (data.pay_periods[index] === true ? 1 : 0)),
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
      footer: totalOfColumn((data) => data.fte),
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
  // State
  const columns = [...employeeColumns, ...monthColumns];
  const [globalFilter, setGlobalFilter] = useState("");
  const [sorting, setSorting] = useState([]);
  const [showPreviousMonths, setShowPreviousMonths] = useState(false);

  // Table state
  const table = useReactTable({
    data,
    columns,
    state: {
      globalFilter,
      sorting,
    },
    filterFns: {
      fuzzy: fuzzyFilter,
    },
    globalFilterFn: "fuzzy",
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
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
      <input
        type="text"
        value={globalFilter}
        onChange={(e) => setGlobalFilter(e.target.value)}
        placeholder="Search by name, grade, employee no..."
        style={{
          marginBottom: "10px",
          marginRight: "10px",
          padding: "5px",
          width: "350px",
        }}
      />
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
        <tfoot>
          {table.getFooterGroups().map((footerGroup) => (
            <tr key={footerGroup.id}>
              {footerGroup.headers.map((footer) => (
                <td key={footer.id}>{footer.column.columnDef.footer}</td>
              ))}
            </tr>
          ))}
        </tfoot>
      </table>
    </div>
  );
}

export default PayrollNewTable;
