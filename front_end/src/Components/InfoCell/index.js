import React from 'react'
import { useSelector } from 'react-redux'

const InfoCell = ({rowIndex, cellKey, children, ignoreSelection}) => {
    const selectedRow = useSelector(state => state.selected.selectedRow)
    const allSelected = useSelector(state => state.selected.all)
    const hiddenCols = useSelector(state => state.hiddenCols.hiddenCols)

    let isHidden = false

    if (cellKey) {
        isHidden = hiddenCols.indexOf(cellKey) > -1
    }

    const isSelected = () => {
        if (ignoreSelection)
            return false

        if (allSelected) {
            return true
        }

        return selectedRow === rowIndex
    }

    const getClasses = () => {
        let hidden = ''

        if (isHidden) {
            hidden = ' hidden'
        }

        return "govuk-table__cell forecast-month-cell not-editable " + (isSelected() ? 'selected' : '') + hidden 
    }

    return (
        <td className={getClasses()}>
            {children}
        </td>
    );
}

export default InfoCell
