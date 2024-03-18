import React from 'react'
import { useSelector } from 'react-redux'

const TableHeader = ({children, colName}) => {
    let changed = false

    const checkValue = (hiddenCols) => {
        if (hiddenCols.indexOf(colName) > -1) {
            changed = true
            return false
        } else if (changed) {
            changed = false
            return false
        }

        return true
    }

    const hiddenCols = useSelector(state => state.hiddenCols.hiddenCols, checkValue)

    return (
        <th
            className={"govuk-table__header " + (hiddenCols.indexOf(colName) > -1 ? 'hidden' : '')}
        >
            {children}
        </th>
    );
}

export default TableHeader
