import React, { Fragment, memo } from "react";
import { useSelector, useDispatch } from "react-redux";
import { nanoid } from "nanoid";
import TableCell from "../../Components/TableCell/index";
import InfoCell from "../../Components/InfoCell/index";
import CellValue from "../../Components/CellValue/index";
import AggregateValue from "../../Components/AggregateValue/index";
import VariancePercentage from "../../Components/VariancePercentage/index";
import TableHeader from "../../Components/TableHeader/index";
import TotalCol from "../../Components/TotalCol/index";
import ToggleCell from "../../Components/ToggleCell/index";
import TotalAggregate from "../../Components/TotalAggregate/index";
import TotalBudget from "../../Components/TotalBudget/index";
import OverspendUnderspend from "../../Components/OverspendUnderspend/index";
import TotalOverspendUnderspend from "../../Components/TotalOverspendUnderspend/index";
import TotalVariancePercentage from "../../Components/TotalVariancePercentage/index";
import ActualsHeaderRow from "../../Components/ActualsHeaderRow/index";
import { getCellId, monthsToTitleCase } from "../../Util";

import { SET_EDITING_CELL } from "../../Reducers/Edit";
import {
  SET_SELECTED_ROW,
  SELECT_ALL,
  UNSELECT_ALL,
} from "../../Reducers/Selected";

function Table({ sheetUpdating }) {
  const dispatch = useDispatch();
  const rows = useSelector((state) => state.allCells.cells);

  const selectedRow = useSelector((state) => state.selected.selectedRow);
  const allSelected = useSelector((state) => state.selected.all);

  return (
    <Fragment>
      <table className="govuk-table finance-table" id="forecast-table">
        <caption className="govuk-table__caption govuk-!-font-size-17">
          Forecast data
        </caption>
        <thead className="govuk-table__head">
          <ActualsHeaderRow />
          <tr index="0">
            <th className="handle govuk-table__cell indicate-action select-all">
              <button
                className="link-button govuk-link"
                id="select_all"
                onMouseDown={() => {
                  dispatch(
                    SET_EDITING_CELL({
                      cellId: null,
                    }),
                  );
                  if (allSelected) {
                    dispatch(UNSELECT_ALL());
                  } else {
                    dispatch(SELECT_ALL());
                  }
                }}
              >
                {allSelected ? (
                  <Fragment>unselect</Fragment>
                ) : (
                  <Fragment>select all</Fragment>
                )}
              </button>
            </th>
            <TableHeader colName="programme_code">Programme code</TableHeader>
            <TableHeader colName="programme_description">
              Programme description
            </TableHeader>
            <TableHeader id="natural_account_code_header" colName="nac_code">
              NAC code
            </TableHeader>
            <TableHeader colName="nac_description">NAC description</TableHeader>
            <TableHeader colName="analysis1_code">
              Contract Reconciliation
            </TableHeader>
            <TableHeader colName="analysis2_code">Markets</TableHeader>
            <TableHeader colName="project_code">Project Code</TableHeader>
            <TableHeader colName="budget">Budget</TableHeader>
            {monthsToTitleCase.map((month) => {
              return (
                <th className="govuk-table__header" key={month}>
                  {month}
                </th>
              );
            })}
            {window.period_display && window.period_display.includes(13) && (
              <th className="govuk-table__header">Adj 1</th>
            )}
            {window.period_display && window.period_display.includes(14) && (
              <th className="govuk-table__header">Adj 2</th>
            )}
            {window.period_display && window.period_display.includes(15) && (
              <th className="govuk-table__header">Adj 3</th>
            )}
            <th className="govuk-table__header">Forecast Outturn</th>
            <th className="govuk-table__header">
              Variance -overspend/underspend
            </th>
            <th className="govuk-table__header">Variance %</th>
            <th className="govuk-table__header">Year to Date Actuals</th>
          </tr>
        </thead>
        <tbody className="govuk-table__body">
          {rows.map((cells, rowIndex) => {
            return (
              <tr key={rowIndex} index={nanoid()}>
                <td
                  id={"select_" + rowIndex}
                  className="handle govuk-table__cell indicate-action"
                >
                  <button
                    className="select_row_btn govuk-link link-button"
                    id={"select_row_" + rowIndex}
                    onMouseDown={() => {
                      dispatch(
                        SET_EDITING_CELL({
                          cellId: null,
                        }),
                      );
                      if (selectedRow === rowIndex) {
                        dispatch(
                          SET_SELECTED_ROW({
                            selectedRow: null,
                          }),
                        );
                      } else {
                        dispatch(
                          SET_SELECTED_ROW({
                            selectedRow: rowIndex,
                          }),
                        );
                      }
                    }}
                  >
                    {selectedRow === rowIndex ? (
                      <Fragment>unselect</Fragment>
                    ) : (
                      <Fragment>select</Fragment>
                    )}
                  </button>
                </td>
                <ToggleCell colName={"programme_code"} rowIndex={rowIndex}>
                  <CellValue rowIndex={rowIndex} cellKey={"programme"} />
                </ToggleCell>

                <ToggleCell
                  colName={"programme_description"}
                  rowIndex={rowIndex}
                >
                  <CellValue
                    rowIndex={rowIndex}
                    cellKey={"programme_description"}
                  />
                </ToggleCell>

                <ToggleCell colName={"nac_code"} rowIndex={rowIndex}>
                  <CellValue
                    rowIndex={rowIndex}
                    cellKey={"natural_account_code"}
                  />
                </ToggleCell>

                <ToggleCell colName={"nac_description"} rowIndex={rowIndex}>
                  <CellValue rowIndex={rowIndex} cellKey={"nac_description"} />
                </ToggleCell>

                <ToggleCell colName={"analysis1_code"} rowIndex={rowIndex}>
                  <CellValue rowIndex={rowIndex} cellKey={"analysis1_code"} />
                </ToggleCell>

                <ToggleCell colName={"analysis2_code"} rowIndex={rowIndex}>
                  <CellValue rowIndex={rowIndex} cellKey={"analysis2_code"} />
                </ToggleCell>

                <ToggleCell colName={"project_code"} rowIndex={rowIndex}>
                  <CellValue rowIndex={rowIndex} cellKey={"project_code"} />
                </ToggleCell>

                <InfoCell
                  className="figure-cell"
                  cellKey={"budget"}
                  rowIndex={rowIndex}
                >
                  <CellValue
                    rowIndex={rowIndex}
                    cellKey={"budget"}
                    format={true}
                  />
                </InfoCell>
                {window.period_display.map((value, index) => {
                  return (
                    <TableCell
                      key={nanoid()}
                      sheetUpdating={sheetUpdating}
                      cellId={getCellId(rowIndex, value)}
                      rowIndex={rowIndex}
                      cellKey={value}
                    />
                  );
                })}
                <InfoCell className="figure-cell" rowIndex={rowIndex}>
                  <AggregateValue
                    rowIndex={rowIndex}
                    actualsOnly={false}
                    extraClasses=""
                  />
                </InfoCell>
                <InfoCell className="figure-cell" rowIndex={rowIndex}>
                  <OverspendUnderspend rowIndex={rowIndex} />
                </InfoCell>
                <InfoCell className="figure-cell" rowIndex={rowIndex}>
                  <VariancePercentage rowIndex={rowIndex} />
                </InfoCell>
                <InfoCell className="figure-cell" rowIndex={rowIndex}>
                  <AggregateValue
                    rowIndex={rowIndex}
                    actualsOnly={true}
                    extraClasses="last-col"
                  />
                </InfoCell>
              </tr>
            );
          })}
          <tr>
            <td className="govuk-table__cell total">Totals</td>
            <InfoCell cellKey={"programme_code"} ignoreSelection={true} />
            <InfoCell
              cellKey={"programme_description"}
              ignoreSelection={true}
            />
            <InfoCell cellKey={"nac_code"} ignoreSelection={true} />
            <InfoCell cellKey={"nac_description"} ignoreSelection={true} />
            <InfoCell cellKey={"analysis1_code"} ignoreSelection={true} />
            <InfoCell cellKey={"analysis2_code"} ignoreSelection={true} />
            <InfoCell cellKey={"project_code"} ignoreSelection={true} />
            <TotalBudget id="total-budget" cellKey={"budget"} />
            {window.period_display &&
              window.period_display.map((value, index) => {
                return <TotalCol key={nanoid()} month={value} />;
              })}
            <TotalAggregate
              actualsOnly={false}
              id="year-total"
              extraClasses=""
            />
            <TotalOverspendUnderspend id="overspend-underspend-total" />
            <TotalVariancePercentage id="variance-total" />
            <TotalAggregate
              actualsOnly={true}
              id="year-to-date"
              extraClasses="last-col"
            />
          </tr>
        </tbody>
      </table>
    </Fragment>
  );
}

const comparisonFn = function (prevProps, nextProps) {
  return prevProps.sheetUpdating === nextProps.sheetUpdating;
};

export default memo(Table, comparisonFn);
