import { useState } from "react";

const EmployeeRow = ({ row }) => {
  const [periods, setPeriods] = useState(
    Object.keys(row)
      .filter((key) => key.includes("period"))
      .map((key) => ({ key: key, value: row[key] }))
  );

  const handleCheckboxChange = (index) => {
    const updatedPeriods = [...periods];
    updatedPeriods[index].value = !updatedPeriods[index].value; // Toggle the checkbox value

    // If checkbox is now unchecked, uncheck all following checkboxes
    if (!updatedPeriods[index].value) { 
      for (let i = index + 1; i < 12; i++) {
        updatedPeriods[i].value = false;
      }
    }

    setPeriods(updatedPeriods);
  };

  return (
    <tr className="govuk-table__row" key={row.employee_no}>
      <td className="govuk-table__cell">{row.name}</td>
      <td className="govuk-table__cell">{row.employee_no}</td>

      {periods.map((period, index) => {
        return (
          <td className="govuk-table__cell" key={period.key}>
            <input
              type="checkbox"
              checked={period.value}
              onChange={() => handleCheckboxChange(index)}
            />
          </td>
        );
      })}
    </tr>
  );
};

export default EmployeeRow;
