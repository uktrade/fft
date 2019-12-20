import React, {Fragment } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import TableCell from '../../Components/TableCell/index'
import TableHeader from '../../Components/TableHeader/index'
import { SET_SELECTED_ROW, SELECT_ALL } from '../../Reducers/Selected'


function Table({rowData}) {
    const dispatch = useDispatch();

    const nac = useSelector(state => state.showHideCols.nac);
    const programme = useSelector(state => state.showHideCols.programme);
    const analysis1 = useSelector(state => state.showHideCols.analysis1);
    const analysis2 = useSelector(state => state.showHideCols.analysis2);
    const projectCode = useSelector(state => state.showHideCols.projectCode);

    const rows = useSelector(state => state.allCells.cells);

    console.log("rows", rows)

    const isHidden = (key) => {
        if (!nac && key === "natural_account_code") {
            return true
        }

        if (!programme && key === "programme") {
            return true
        }

        if (!analysis1 && key === "analysis1_code") {
            return true
        }

        if (!analysis2 && key === "analysis2_code") {
            return true
        }

        if (!projectCode && key === "project_code") {
            return true
        }

        return false
    }

    return (
        <Fragment>
            <table
                className="govuk-table" id="forecast-table">
                <caption className="govuk-table__caption">Edit forecast</caption>
                <thead className="govuk-table__head">
                    <tr index="0">
                        <td id="select_all" className="handle govuk-table__cell indicate-action"
                            onClick={() => { 
                                dispatch(
                                    SELECT_ALL()
                                );
                            }
                        }>
                            select all
                        </td>
                        <TableHeader isHidden={isHidden} id="natural_account_code_header" headerType="natural_account_code">Natural Account Code</TableHeader>
                        <TableHeader isHidden={isHidden} headerType="programme">Programme</TableHeader>
                        <TableHeader isHidden={isHidden} headerType="analysis1_code">Analysis Code Sector</TableHeader>
                        <TableHeader isHidden={isHidden} headerType="analysis2_code">Analysis Code Market</TableHeader>
                        <TableHeader isHidden={isHidden} headerType="project_code">Project Code</TableHeader>
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
                        return <tr key={rowIndex} index={(rowIndex + 1)}>
                            <td id={"select_" + rowIndex}  className="handle govuk-table__cell indicate-action"
                                onClick={() => { 
                                    console.log(rowIndex)
                                    dispatch(
                                        SET_SELECTED_ROW({
                                            selectedRow: rowIndex
                                        })
                                    );
                                }
                            }>
                                select
                            </td>
                            <TableCell rowIndex={rowIndex} isHidden={isHidden} cellKey={"natural_account_code"} />
                            <TableCell rowIndex={rowIndex} isHidden={isHidden} cellKey={"programme"} />
                            <TableCell rowIndex={rowIndex} isHidden={isHidden} cellKey={"analysis1_code"} />
                            <TableCell rowIndex={rowIndex} isHidden={isHidden} cellKey={"analysis2_code"} />
                            <TableCell rowIndex={rowIndex} isHidden={isHidden} cellKey={"project_code"} />
                            <TableCell rowIndex={rowIndex} cellKey={"apr"} />
                            <TableCell rowIndex={rowIndex} cellKey={"may"} />
                            <TableCell rowIndex={rowIndex} cellKey={"jun"} />
                            <TableCell rowIndex={rowIndex} cellKey={"jul"} />
                            <TableCell rowIndex={rowIndex} cellKey={"aug"} />
                            <TableCell rowIndex={rowIndex} cellKey={"sep"} />
                            <TableCell rowIndex={rowIndex} cellKey={"oct"} />
                            <TableCell rowIndex={rowIndex} cellKey={"nov"} />
                            <TableCell rowIndex={rowIndex} cellKey={"dec"} />
                            <TableCell rowIndex={rowIndex} cellKey={"jan"} />
                            <TableCell rowIndex={rowIndex} cellKey={"feb"} />
                            <TableCell rowIndex={rowIndex} cellKey={"mar"} />
                        </tr>
                    })}
                </tbody>
            </table>
        </Fragment>
    );
}

export default Table
