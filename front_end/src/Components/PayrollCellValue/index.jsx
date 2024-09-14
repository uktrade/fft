import React, {Fragment} from 'react'
import { useSelector } from 'react-redux'

import {
    formatValue
} from '../../Util'

const PayrollCellValue = ({rowIndex, cellKey, format}) => {
    console.log("PayrollCellValue component has been rendered");
    console.log("rowIndex: ", rowIndex);
    console.log("cellKey: ", cellKey);
    console.log("format: ", format);
    const cell = useSelector(state => state.allCells.employeeCells[rowIndex][cellKey]);

    const getValue = (value) => {
        if (format) {
            return formatValue(parseInt(value, 10)/100)
        }

        return value
    }

    return (
        <Fragment>
            {getValue(cell.value)}
        </Fragment>
    )
}

export default PayrollCellValue
