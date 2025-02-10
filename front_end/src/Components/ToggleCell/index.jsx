import React from "react";
import { useSelector } from "react-redux";

const ToggleCell = ({ rowIndex, colName, children }) => {
  const isRowSelected = useSelector(
    (state) => state.selected.all || state.selected.selectedRow === rowIndex,
  );
  const isColHidden = useSelector(
    (state) => state.hiddenCols.hiddenCols.indexOf(colName) > -1,
  );

  const getClasses = () => {
    return (
      "govuk-table__cell forecast-month-cell not-editable " +
      (isRowSelected ? "selected " : "") +
      (isColHidden ? "hidden" : "")
    );
  };

  return <td className={getClasses()}>{children}</td>;
};

export default ToggleCell;
