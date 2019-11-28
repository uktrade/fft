import React, {Fragment } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import TableCell from '../../Components/TableCell/index'
import TableHeader from '../../Components/TableHeader/index'
import { SET_SELECTED_ROW, SELECT_ALL } from '../../Reducers/Selected'


function Table({rowData}) {
    const dispatch = useDispatch();

    const nac = useSelector(state => state.showHideCols.nac);
    const programme = useSelector(state => state.showHideCols.programme);
    // const analysis1 = useSelector(state => state.showHideCols.analysis1);
    // const analysis2 = useSelector(state => state.showHideCols.analysis2);
    const projectCode = useSelector(state => state.showHideCols.projectCode);

    const isHidden = (key) => {
        if (!nac && key === "cost_centre__cost_centre_code") {
            return true
        }

        if (!programme && key === "programme__programme_code") {
            return true
        }

        // if (!analysis1 && key === "cost_centre__cost_centre_code") {
        //     return true
        // }

        // if (!analysis2 && key === "cost_centre__cost_centre_code") {
        //     return true
        // }

        if (!projectCode && key === "project_code__project_code") {
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
                        <td className="handle govuk-table__cell indicate-action"
                            onClick={() => { 
                                dispatch(
                                    SELECT_ALL()
                                );
                            }
                        }>
                            select all
                        </td>
                        <TableHeader isHidden={isHidden} headerType="natural_account_code__natural_account_code">Natural Account Code</TableHeader>
                        <TableHeader isHidden={isHidden} headerType="programme__programme_code">Programme</TableHeader>
                        <TableHeader isHidden={isHidden} headerType="a1">Analysis Code Sector</TableHeader>
                        <TableHeader isHidden={isHidden} headerType="a2">Analysis Code Market</TableHeader>
                        <TableHeader isHidden={isHidden} headerType="project_code__project_code">Project Code</TableHeader>
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
                    {rowData.map((cells, rowIndex) => {
                        return <tr key={rowIndex} index={(rowIndex + 1)}>
                            <td className="handle govuk-table__cell indicate-action"
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
                            <TableCell isHidden={isHidden} cell={cells["natural_account_code__natural_account_code"]} />
                            <TableCell isHidden={isHidden} cell={cells["programme__programme_code"]} />
                            <TableCell isHidden={isHidden} cell={cells["analysis1_code__analysis1_code"]} />
                            <TableCell isHidden={isHidden} cell={cells["analysis2_code__analysis2_code"]} />
                            <TableCell isHidden={isHidden} cell={cells["project_code__project_code"]} />
                            <TableCell cell={cells["Apr"]} />
                            <TableCell cell={cells["May"]} />
                            <TableCell cell={cells["Jun"]} />
                            <TableCell cell={cells["Jul"]} />
                            <TableCell cell={cells["Aug"]} />
                            <TableCell cell={cells["Sep"]} />
                            <TableCell cell={cells["Oct"]} />
                            <TableCell cell={cells["Nov"]} />
                            <TableCell cell={cells["Dec"]} />
                            <TableCell cell={cells["Jan"]} />
                            <TableCell cell={cells["Feb"]} />
                            <TableCell cell={cells["Mar"]} />
                        </tr>
                    })}
                </tbody>
            </table>
        </Fragment>
    );
}

export default Table
