import React, {Fragment, memo } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { nanoid } from 'nanoid'
import PayrollTableCell from '../../Components/PayrollTableCell/index'
import InfoCell from '../../Components/InfoCell/index'
import CellValue from '../../Components/CellValue/index'
import TableHeader from '../../Components/TableHeader/index'
import ToggleCell from '../../Components/ToggleCell/index'
import ActualsHeaderRow from '../../Components/ActualsHeaderRow/index'
import {
    getCellId
} from '../../Util'

import { SET_EDITING_CELL } from '../../Reducers/Edit'
import { SET_SELECTED_ROW, SELECT_ALL, UNSELECT_ALL } from '../../Reducers/Selected'


function Table({rowData, sheetUpdating}) {
    const dispatch = useDispatch();
    const rows = useSelector(state => state.allCells.cells);

    const selectedRow = useSelector(state => state.selected.selectedRow);
    const allSelected = useSelector(state => state.selected.all);

    return (
        <Fragment>
            <table
                className="govuk-table payroll-non-table" id="payroll-non-table">
                <caption className="govuk-table__caption govuk-!-font-size-17">Non Payroll data</caption>
                <thead className="govuk-table__head">
                    <ActualsHeaderRow />
                    <tr index="0">
                        <th className="handle govuk-table__cell indicate-action select-all">
                            <button className="link-button govuk-link"
                                    id="select_all"
                                    onMouseDown={() => {
                                        dispatch(
                                            SET_EDITING_CELL({
                                                "cellId": null
                                            })
                                        )
                                        if (allSelected) {
                                            dispatch(
                                                UNSELECT_ALL()
                                            )
                                        } else {
                                            dispatch(
                                                SELECT_ALL()
                                            )
                                        }
                                    }
                                    }>
                                {allSelected ? (
                                    <Fragment>unselect</Fragment>
                                ) : (
                                    <Fragment>select all</Fragment>
                                )}
                            </button>
                        </th>
                        <TableHeader colName="name">Name</TableHeader>
                        <TableHeader colName="grade">Grade</TableHeader>
                        <TableHeader colName="staff_number">Staff number</TableHeader>
                        <TableHeader colName="fte">FTE</TableHeader>
                        <TableHeader colName="programme_code">Programme Code</TableHeader>
                        <TableHeader colName="budget_type">Budget type</TableHeader>
                        <TableHeader colName="eu_non_eu">EU/Non-EU</TableHeader>
                        <TableHeader colName="assignment_status">Assignment status</TableHeader>
                        <th className="govuk-table__header">Apr</th>
                        <th className="govuk-table__header">May</th>
                        <th className="govuk-table__header">Jun</th>
                        <th className="govuk-table__header">Jul</th>
                        <th className="govuk-table__header">Aug</th>
                        <th className="govuk-table__header">Sep</th>
                        <th className="govuk-table__header">Oct</th>
                        <th className="govuk-table__header">Nov</th>
                        <th className="govuk-table__header">Dec</th>
                        <th className="govuk-table__header">Jan</th>
                        <th className="govuk-table__header">Feb</th>
                        <th className="govuk-table__header">Mar</th>
                    </tr>
                </thead>
                <tbody className="govuk-table__body">
                {rows.map((cells, rowIndex) => {
                    return <tr key={rowIndex} index={nanoid()}>
                        <td id={"select_" + rowIndex} className="handle govuk-table__cell indicate-action">
                            <button
                                className="select_row_btn govuk-link link-button"
                                id={"select_row_" + rowIndex}
                                onMouseDown={() => {
                                    dispatch(
                                        SET_EDITING_CELL({
                                            "cellId": null
                                        })
                                    )
                                    if (selectedRow === rowIndex) {
                                            dispatch(
                                                SET_SELECTED_ROW({
                                                    selectedRow: null
                                                })
                                            )
                                        } else {
                                            dispatch(
                                                SET_SELECTED_ROW({
                                                    selectedRow: rowIndex
                                                })
                                            )
                                        }
                                    }
                                }>
                                    {selectedRow === rowIndex ? (
                                        <Fragment>unselect</Fragment>
                                    ) : (
                                        <Fragment>select</Fragment>
                                    )}
                                </button>
                            </td>
                            <ToggleCell colName={"name"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"name"} />
                            </ToggleCell>
                            <InfoCell className="figure-cell" cellKey={"fte"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"fte"} />
                            </InfoCell>
                            <InfoCell className="figure-cell" cellKey={"staff_number"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"staff_number"} />
                            </InfoCell>
                            <InfoCell className="figure-cell" cellKey={"grade"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"grade"} />
                            </InfoCell>
                            <InfoCell className="figure-cell" cellKey={"programme_code"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"programme_code"} />
                            </InfoCell>
                            <InfoCell className="figure-cell" cellKey={"budget_type"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"budget_type"} />
                            </InfoCell>
                            <InfoCell className="figure-cell" cellKey={"eu_non_eu"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"eu_non_eu"} />
                            </InfoCell>
                            <InfoCell className="figure-cell" cellKey={"assignment_status"} rowIndex={rowIndex}>
                                <CellValue rowIndex={rowIndex} cellKey={"assignment_status"} />
                            </InfoCell>
                            {Object.keys(window.payroll_non_employee_monthly_data).map((dataKey, index) => {
                                const monthValues = window.payroll_non_employee_monthly_data[dataKey]; // Access the month object (e.g., { "apr": 1, "may": 1, ... })

                                if (rowIndex === index) {
                                    return (
                                    Object.keys(monthValues).map((monthKey) => {
                                        const monthValue = monthValues[monthKey]; // Access the value for each month
                                        return (
                                            <PayrollTableCell
                                                key={nanoid()}
                                                sheetUpdating={sheetUpdating}
                                                cellId={getCellId(rowIndex, `${dataKey}_${monthKey}`)} // Unique ID based on dataKey and monthKey
                                                rowIndex={rowIndex}
                                                cellKey={monthKey} // Pass the monthKey (e.g., "apr")
                                                cellValue={monthValue}
                                            >
                                            </PayrollTableCell>
                                        );
                                    })
                                );
                                }


                            })}
                        </tr>

                    })}
                </tbody>
            </table>
        </Fragment>
    );
}

const comparisonFn = function(prevProps, nextProps) {
    return (
        prevProps.sheetUpdating === nextProps.sheetUpdating
    )
};


export default memo(Table, comparisonFn);
