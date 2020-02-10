import React, { memo } from 'react'
import { useSelector } from 'react-redux'

const InfoCell = ({rowIndex, cellKey, children, className, ignoreSelection}) => {
    const selectedRow = useSelector(state => state.selected.selectedRow)
    const allSelected = useSelector(state => state.selected.all)

    const isSelected = () => {
        if (ignoreSelection)
            return false

        if (allSelected) {
            return true
        }

        return selectedRow === rowIndex
    }

    const getClasses = () => {
        return "govuk-table__cell forecast-month-cell not-editable " + className + " " + (isSelected() ? 'selected' : '') 
    }

    return (
        <td className={getClasses()}>
            {children}
        </td>
    );
}


const comparisonFn = function(prevProps, nextProps) {
    return (
        prevProps.selectedRow === nextProps.selectedRow &&
        prevProps.allSelected === nextProps.allSelected
    )
};

export default memo(InfoCell, comparisonFn);

