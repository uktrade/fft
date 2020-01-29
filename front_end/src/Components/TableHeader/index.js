import React from 'react'
import { useSelector } from 'react-redux'

const TableHeader = ({children, headerType}) => {
    const hiddenCols = useSelector(state => state.hiddenCols.hiddenCols)
    const isHidden = hiddenCols.indexOf(headerType) > -1

    return (
        <th
            className={"govuk-table__header " + (isHidden ? 'hidden' : '')}
        >
            {children}
        </th>
    );
}

export default TableHeader
