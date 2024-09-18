import React, {Fragment, memo } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { nanoid } from 'nanoid'
import TableHeader from '../../Components/TableHeader/index'
import ToggleCell from '../../Components/ToggleCell/index'
import {
    getCellId
} from '../../Util'

import { SET_EDITING_CELL } from '../../Reducers/Edit'
import {
    SET_MYHR_EMPLOYEE_SELECTED_ROW
} from '../../Reducers/Selected'
import PayrollCellValue from "../PayrollCellValue/index.jsx";
import MyHREmployeeTableCell from "../MyHREmployeeTableCell/index.jsx";
import ActualsWithoutForecastHeaderRow from "../ActualsWithForecastHeaderRow/index.jsx";
import MyHREmployeeCellValue from "../MyHREmployeeCellValue/index.jsx";


function Table({rowData, sheetUpdating}) {
    const dispatch = useDispatch();
    const rows = useSelector(state => state.allCells.myhrEmployeeCells);

    const selectedRow = useSelector(state => state.selected.myHREmployeeSelectedRow);
    const allSelected = useSelector(state => state.selected.all);

    return (
        <Fragment>
            <table
                className="govuk-table myhr-employee-table" id="myhr-employee-table">
                <caption className="govuk-table__caption govuk-!-font-size-17">MyHR Employee Group table</caption>
                <thead className="govuk-table__head">
                    <ActualsWithoutForecastHeaderRow />
                    <tr index="0">
                        <TableHeader colName="group">Name</TableHeader>
                        <TableHeader colName="fte">FTE</TableHeader>
                        <TableHeader colName="count">Count</TableHeader>
                    </tr>
                </thead>
                <tbody className="govuk-table__body">
                {rows.map((cells, rowIndex) => {
                    return <tr key={rowIndex} index={nanoid()}>
                        {/*<td id={"select_" + rowIndex} className="handle govuk-table__cell indicate-action">*/}
                            {/*<button*/}
                            {/*    className="select_row_btn govuk-link link-button"*/}
                            {/*    id={"select_row_" + rowIndex}*/}
                            {/*    onMouseDown={() => {*/}
                            {/*        dispatch(*/}
                            {/*            SET_EDITING_CELL({*/}
                            {/*                "cellId": null*/}
                            {/*            })*/}
                            {/*        )*/}
                            {/*        if (selectedRow === rowIndex) {*/}
                            {/*                dispatch(*/}
                            {/*                    SET_MYHR_EMPLOYEE_SELECTED_ROW({*/}
                            {/*                        myHREmployeeSelectedRow: null*/}
                            {/*                    })*/}
                            {/*                )*/}
                            {/*            } else {*/}
                            {/*                dispatch(*/}
                            {/*                    SET_MYHR_EMPLOYEE_SELECTED_ROW({*/}
                            {/*                        myHREmployeeSelectedRow: rowIndex*/}
                            {/*                    })*/}
                            {/*                )*/}
                            {/*            }*/}
                            {/*        }*/}
                            {/*    }>*/}
                            {/*        {selectedRow === rowIndex ? (*/}
                            {/*            <Fragment>unselect</Fragment>*/}
                            {/*        ) : (*/}
                            {/*            <Fragment>select</Fragment>*/}
                            {/*        )}*/}
                            {/*    </button>*/}
                            {/*</td>*/}
                            <ToggleCell colName={"group"} rowIndex={rowIndex}>
                                <MyHREmployeeCellValue rowIndex={rowIndex} cellKey={"group"} view_name={"directorate"} />
                            </ToggleCell>
                            <ToggleCell colName={"fte"} rowIndex={rowIndex}>
                                <MyHREmployeeCellValue rowIndex={rowIndex} cellKey={"fte"} />
                            </ToggleCell>
                            <ToggleCell colName={"count"} rowIndex={rowIndex}>
                                <MyHREmployeeCellValue rowIndex={rowIndex} cellKey={"count"} />
                            </ToggleCell>
                            {/*{Object.keys(window.payroll_employee_monthly_data).map((dataKey, index) => {*/}
                            {/*    const monthValues = window.payroll_employee_monthly_data[dataKey]; // Access the month object (e.g., { "apr": 1, "may": 1, ... })*/}
                            {/*    if (rowIndex === index) {*/}
                            {/*        return (*/}
                            {/*            Object.keys(monthValues).map((monthKey) => {*/}
                            {/*                const monthValue = monthValues[monthKey]; // Access the value for each month*/}
                            {/*                return (*/}
                            {/*                    <MyHREmployeeTableCell*/}
                            {/*                        key={nanoid()}*/}
                            {/*                        sheetUpdating={sheetUpdating}*/}
                            {/*                        cellId={getCellId(rowIndex, `pe_${dataKey}_${monthKey}`)} // Unique ID based on dataKey and monthKey*/}
                            {/*                        rowIndex={rowIndex}*/}
                            {/*                        cellKey={monthKey} // Pass the monthKey (e.g., "apr")*/}
                            {/*                        cellValue={monthValue}*/}
                            {/*                    >*/}
                            {/*                    </MyHREmployeeTableCell>*/}
                            {/*                );*/}
                            {/*            })*/}
                            {/*        );*/}
                            {/*    }*/}
                            {/*})}*/}
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
