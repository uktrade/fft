import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  getFilteredRowModel,
  getSortedRowModel,
} from "@tanstack/react-table";
import { rankItem } from "@tanstack/match-sorter-utils";
import { monthsToTitleCase } from "../../../Util";
import { useState } from "react";

const fuzzyFilter = (row, columnId, value, addMeta) => {
  const itemRank = rankItem(row.getValue(columnId), value);
  addMeta({ itemRank });
  return itemRank.passed;
};

function TanstackTable({ data, onTogglePayPeriods }) {
  const monthColumns = monthsToTitleCase.map((header, index) => ({
    header: header,
    id: header.toLowerCase(),
    enableSorting: false,
    enableHiding: false,
    accessorFn: (row) => row.pay_periods[index],
    cell: ({ getValue, row }) => (
      <input
        type="checkbox"
        checked={getValue()}
        onChange={() => onTogglePayPeriods(row.original.id, index, getValue())}
      />
    ),
  }));
  const columns = [
    {
      accessorKey: "name",
      header: "Name",
      filterFn: "includesString",
      enableHiding: true,
    },
    {
      accessorKey: "grade",
      header: "Grade",
      enableHiding: true,
    },
    {
      accessorKey: "employee_no",
      header: "Employee No",
      filterFn: "includesString",
      enableHiding: true,
    },
    {
      accessorKey: "fte",
      header: "FTE",
      enableHiding: true,
    },
    {
      accessorKey: "programme_code",
      header: "Programme Code",
      enableHiding: true,
    },
    {
      accessorKey: "budget_type",
      header: "Budget Type",
      enableHiding: true,
    },
    {
      accessorKey: "assignment_status",
      header: "Assignment Status",
      enableHiding: true,
    },
    ...monthColumns,
  ];
  const [globalFilter, setGlobalFilter] = useState("");
  const [sorting, setSorting] = useState([]);
  const [columnVisibility, setColumnVisibility] = useState({});

  const table = useReactTable({
    data,
    columns,
    filterFns: {
      fuzzy: fuzzyFilter,
    },
    state: {
      globalFilter,
      sorting,
      columnVisibility,
    },
    onGlobalFilterChange: setGlobalFilter,
    globalFilterFn: "fuzzy",
    onSortingChange: setSorting,
    onColumnVisibilityChange: setColumnVisibility,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <div className="tanstack scrollable">
      <div className="checkboxes">
        <label>
          <input
            {...{
              type: "checkbox",
              checked: table.getIsAllColumnsVisible(),
              onChange: table.getToggleAllColumnsVisibilityHandler(),
            }}
          />{" "}
          Toggle all
        </label>
        {table.getAllColumns().map((column) => {
          return column.columnDef.enableHiding ? (
            <div key={column.id}>
              <label>
                <input
                  {...{
                    type: "checkbox",
                    checked: column.getIsVisible(),
                    onChange: column.getToggleVisibilityHandler(),
                  }}
                />{" "}
                {column.columnDef.header}
              </label>
            </div>
          ) : null;
        })}
      </div>
      <input
        type="text"
        value={globalFilter}
        onChange={(e) => setGlobalFilter(e.target.value)}
        placeholder="Search by name, employee no.."
        className="govuk-input"
        style={{
          marginBottom: "10px",
          padding: "5px",
          width: "20%",
          fontSize: "16px",
        }}
      />
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
                    asc: " ↑",
                    desc: " ↓",
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

export default TanstackTable;
