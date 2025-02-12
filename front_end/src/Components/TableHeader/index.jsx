import React from "react";
import { useSelector } from "react-redux";

const TableHeader = ({ children, colName }) => {
  const isColHidden = useSelector(
    (state) => state.hiddenCols.hiddenCols.indexOf(colName) > -1,
  );

  return (
    <th className={"govuk-table__header " + (isColHidden ? "hidden" : "")}>
      {children}
    </th>
  );
};

export default TableHeader;
