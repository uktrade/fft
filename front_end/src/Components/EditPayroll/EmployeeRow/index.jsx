import { useState } from "react";

const EmployeeRow = ({ row, onTogglePayPeriods }) => {
  return (
    <tr className="govuk-table__row">
      <td className="govuk-table__cell">{row.name}</td>
      <td className="govuk-table__cell">{row.grade}</td>
      <td className="govuk-table__cell">{row.employee_no}</td>
      <td className="govuk-table__cell">{row.fte}</td>
      <td className="govuk-table__cell">{row.programme_code}</td>
      <td className="govuk-table__cell">{row.budget_type}</td>
      <td className="govuk-table__cell">{row.assignment_status}</td>
      {row.pay_periods.map((enabled, index) => {
        return (
          <td className="govuk-table__cell" key={index}>
            <input
              type="checkbox"
              checked={enabled}
              onChange={() =>
                onTogglePayPeriods(row.employee_no, index, enabled)
              }
            />
          </td>
        );
      })}
    </tr>
  );
};

export default EmployeeRow;
