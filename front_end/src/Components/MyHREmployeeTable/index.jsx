import React, {Fragment, memo } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { nanoid } from 'nanoid'
import TableHeader from '../../Components/TableHeader/index'
import ToggleCell from '../../Components/ToggleCell/index'
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
                        <ToggleCell colName={"group"} rowIndex={rowIndex}>
                            <MyHREmployeeCellValue rowIndex={rowIndex} cellKey={"group"} view_name={window.myhr_next_view} />
                        </ToggleCell>
                        <ToggleCell colName={"fte"} rowIndex={rowIndex}>
                            <MyHREmployeeCellValue rowIndex={rowIndex} cellKey={"fte"} />
                        </ToggleCell>
                        <ToggleCell colName={"count"} rowIndex={rowIndex}>
                            <MyHREmployeeCellValue rowIndex={rowIndex} cellKey={"count"} />
                        </ToggleCell>
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
