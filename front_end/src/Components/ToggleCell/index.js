import React from 'react'
import { useSelector } from 'react-redux'

const ToggleCell = ({rowIndex, colName, children}) => {

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

    let selectChanged = false

    const checkSelectRow = (selectedRow) => {
        if (selectedRow === rowIndex) {
            selectChanged = true
            return false
        } else if (selectChanged) {
            selectChanged = false
            return false
        }

        return true
    }

    const selectedRow = useSelector(state => state.selected.selectedRow, checkSelectRow)
    const allSelected = useSelector(state => state.selected.all)
    const hiddenCols = useSelector(state => state.hiddenCols.hiddenCols, checkValue)

    const isSelected = () => {
        if (allSelected) {
            return true
        }

        return selectedRow === rowIndex
    }

    const getClasses = () => {
        return "govuk-table__cell forecast-month-cell not-editable " + (isSelected() ? 'selected ' : '')  + (hiddenCols.indexOf(colName) > -1 ? 'hidden' : '')
    }

    return (
        <td className={getClasses()}>
            {children}
        </td>
    );
}

export default ToggleCell


