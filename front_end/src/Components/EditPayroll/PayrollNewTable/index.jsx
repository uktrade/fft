import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  getFilteredRowModel,
  getSortedRowModel,
} from "@tanstack/react-table";
import { useState } from "react";
import { monthsWithActuals } from "./helpers";
import { rankItem } from "@tanstack/match-sorter-utils";

function PayrollNewTable({ data, columns, previousMonths }) {
  // Column helpers
  // Documentation: https://tanstack.com/table/v8/docs/guide/fuzzy-filtering
  const fuzzyFilter = (row, columnId, value, addMeta) => {
    const itemRank = rankItem(row.getValue(columnId), value);
    addMeta({ itemRank });
    return itemRank.passed;
  };

  // State
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
