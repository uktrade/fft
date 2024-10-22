import { useState } from "react";

const EmployeeRow = ({ row, onTogglePayPeriods }) => {
  return (
    <tr className="govuk-table__row">
      <td className="govuk-table__cell">{row.name}</td>
      <td className="govuk-table__cell">{row.employee_no}</td>
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
