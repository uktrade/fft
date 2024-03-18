import React, {Fragment} from 'react'
import { useSelector } from 'react-redux'

import {
    formatValue
} from '../../Util'

const CellValue = ({rowIndex, cellKey, format}) => {
    const cell = useSelector(state => state.allCells.cells[rowIndex][cellKey]);

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

export default CellValue
