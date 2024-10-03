import React, {Fragment} from 'react'
import { useSelector } from 'react-redux'

import {
    formatValue
} from '../../Util'

const MyHREmployeeCellValue = ({rowIndex, cellKey, format, view_name }) => {
    const cell = useSelector(state => state.allCells.myhrEmployeeCells[rowIndex][cellKey]);

    const getValue = (value) => {
        if (format) {
            return formatValue(parseInt(value, 10)/100)
        }

        // Check if the cellKey is "group" to make it a link
        if (cellKey === 'group' && view_name) {
            const navigate_to_view = `/myhr/${view_name}/`;
            const url = new URL(navigate_to_view, window.location.origin);
            url.searchParams.append('group_name', value);
            return <a href={url.toString()} rel="noopener noreferrer">{value}</a>;
        }

        return value
    }

    return (
        <Fragment>
            {getValue(cell.value)}
        </Fragment>
    )
}

export default MyHREmployeeCellValue
