import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  getFilteredRowModel,
  getSortedRowModel,
} from "@tanstack/react-table";
import { useState } from "react";
import { fuzzyFilter, monthsWithActuals } from "./helpers";
import SortUpIcon from "../../../../icons/sort-up.svg?react";
import SortDownIcon from "../../../../icons/sort-down.svg?react";
import UnsortedIcon from "../../../../icons/unsorted.svg?react";
import ToggleCheckbox from "../../Common/ToggleCheckbox";

function TanstackTable({ data, columns, previousMonths }) {
  // State
  const [globalFilter, setGlobalFilter] = useState("");
  const [sorting, setSorting] = useState([]);
  const [showPreviousMonths, setShowPreviousMonths] = useState(true);

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
    <div className="tanstack-table scrollable">
      <div className="table-options">
        <div className="govuk-form-group">
          <label className="govuk-label" htmlFor="search">
            Search
          </label>
          <input
            type="text"
            id="search"
            value={globalFilter}
            onChange={(e) => setGlobalFilter(e.target.value)}
            placeholder="Search rows..."
            className="search-input"
          />
        </div>
        <ToggleCheckbox
          toggle={showPreviousMonths}
          handler={togglePreviousMonthsVisibility}
          id="payroll-previous-months"
          value="payroll-previous-months"
          label="Show previous months"
        />
      </div>
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
                    asc: <SortUpIcon className="table-svg" />,
                    desc: <SortDownIcon className="table-svg" />,
                    false: header.column.getCanSort() ? (
                      <UnsortedIcon className="table-svg" />
                    ) : null,
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

export default TanstackTable;
