import React from 'react'

const TableHeader = ({children, headerType, isHidden}) => {
    return (
            <th
                className={"govuk-table__header " + (isHidden(headerType) ? 'hidden' : '')}
            >
                {children}
            </th>
    );
}

export default TableHeader
