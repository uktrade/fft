import React from 'react'
import { useSelector } from 'react-redux'

const InfoCell = ({isHidden, rowIndex, cellKey, cellMonth}) => {
    const cell = useSelector(state => state.allCells.cells[rowIndex][cellKey]);
    const selectedRow = useSelector(state => state.selected.selectedRow);
    const allSelected = useSelector(state => state.selected.all);

    const isSelected = () => {
        if (allSelected) {
            return true
        }

        return selectedRow === rowIndex
    }

    const getClasses = () => {
        let hiddenResult = ''

        if (isHidden) {
            hiddenResult = isHidden(cellKey) ? ' hidden' : ''
        }

        return "govuk-table__cell forecast-month-cell not-editable " + (isSelected() ? 'selected' : '') + hiddenResult 
    }

    return (
        <td className={getClasses()}>
            {cell.value}
        </td>
    );
}

export default InfoCell
