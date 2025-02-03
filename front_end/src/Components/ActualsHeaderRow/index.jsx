import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";

const ActualsHeaderRow = () => {
  const [actualsCount, setActualsCount] = useState(0);

  const hiddenColsCount = useSelector(
    (state) => state.hiddenCols.hiddenCols.length,
  );

  // Number of columns from Select All to Budget
  const colsBeforeMonths = 9;
  // Number of columns from Apr to Variance %
  const forecastColCount = 18;

  useEffect(() => {
    const timer = () => {
      setTimeout(() => {
        if (window.actuals) {
          if (window.actuals.length > 0) {
            setActualsCount(window.actuals.length);
          }
        } else {
          timer();
        }
      }, 100);
    };
    timer();
  }, []);

  return (
    <tr>
      <th
        className="govuk-table__head meta-col"
        colSpan={colsBeforeMonths - hiddenColsCount}
      ></th>
      {actualsCount > 0 && (
        <th
          id="actuals_header"
          className="govuk-table__head meta-col"
          colSpan={actualsCount}
        >
          Actuals
        </th>
      )}
      <th
        className="govuk-table__head meta-col"
        colSpan={forecastColCount - actualsCount}
      >
        Forecast
      </th>
    </tr>
  );
};

export default ActualsHeaderRow;
