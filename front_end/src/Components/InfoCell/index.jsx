import React, { memo } from "react";
import { useSelector } from "react-redux";

const InfoCell = ({
  rowIndex,
  cellKey,
  children,
  className,
  ignoreSelection,
}) => {
  const isRowSelected = useSelector(
    (state) => state.selected.all || state.selected.selectedRow === rowIndex,
  );
  const isColHidden = useSelector(
    (state) => state.hiddenCols.hiddenCols.indexOf(cellKey) > -1,
  );

  const getClasses = () => {
    return (
      "govuk-table__cell forecast-month-cell not-editable " +
      className +
      " " +
      (!ignoreSelection && isRowSelected ? "selected " : "") +
      (isColHidden ? "hidden" : "")
    );
  };

  return <td className={getClasses()}>{children}</td>;
};

export default InfoCell;
