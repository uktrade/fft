import React, {Fragment, useState, useEffect, memo } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { SET_EDITING_CELL } from '../../Reducers/Edit'
import {
    formatValue,
    postData,
} from '../../Util'
import { SET_ERROR } from '../../Reducers/Error'

const MyHRTableCell = ({rowIndex, cellId, cellKey, sheetUpdating, cellValue}) => {
    let editing = false
    let isEditable = true

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

    const dispatch = useDispatch();

    const cells = useSelector(state => state.allCells.myhrEmployeeCells);
    const cell = useSelector(state => state.allCells.myhrEmployeeCells[rowIndex][cellKey]);
    const editCellId = useSelector(state => state.edit.cellId, checkValue);

    const [isUpdating, setIsUpdating] = useState(false)

    const selectedRow = useSelector(state => state.selected.myHREmployeeSelectedRow, checkSelectRow);
    const allSelected = useSelector(state => state.selected.all);


    const getValue = () => {
        return cellValue
    }

    const [value, setValue] = useState(getValue())

    useEffect(() => {
        if (cell) {
            setValue(cell)
        }
    }, [cell]);

    const isSelected = () => {
        if (allSelected) {
            return true
        }

        return selectedRow === rowIndex
    }

    const wasEdited = () => {
        return isEditable;
    }

    const getClasses = () => {
        let editable = ''

        if (!isEditable) {
            editable = ' not-editable'
        }

        if (!cell)
            return "govuk-table__cell payroll-month-cell figure-cell " + (isSelected() ? 'selected' : '') + editable

        // let negative = ''

        // if (cell.amount < 0) {
        //     negative = " negative"
        // }

        return "govuk-table__cell payroll-month-cell figure-cell " + (wasEdited() ? 'edited ' : '') + (isSelected() ? 'selected' : '')  + editable + negative
    }

    const setContentState = (value) => {
        // var re = /^-?\d*\.?\d{0,12}$/;
        // var isValid = (value.match(re) !== null);
        //
        // if (!isValid) {
        //     return
        // }
        setValue(value)
    }

    const handleBlur = (event) => {
        updateValue()
        dispatch(
            SET_EDITING_CELL({
                "cellId": null
            })
        )
    }

    const handleKeyDown = (event) => {
        if (event.key === "Tab") {
            updateValue()
        }
    }

    const handleKeyPress = (event) => {
        if(event.key === 'Enter') {
            updateValue()
            event.preventDefault()
        }
    }

    const getId = () => {
        if (!cell)
            return

        if (isUpdating) {
            return cellId + "_updating"
        }

        return cellId
    }

    const isCellUpdating = () => {
        if (cell && !isEditable)
            return false

        if (isUpdating)
            return true

        if (sheetUpdating && isSelected()) {
            return true
        }

        return false
    }

    const getCellContent = () => {
        if (isCellUpdating()) {
            return (
                <Fragment>
                    <span className="updating">UPDATING...</span>
                </Fragment>
            )
        } else {
            if (editCellId === cellId) {
                return (
                    <input
                        ref={input => input && input.focus() }
                        id={cellId + "_input"}
                        className="cell-input"
                        type="text"
                        value={value}
                        onChange={e => setContentState(e.target.value)}
                        onKeyPress={handleKeyPress}
                        onKeyDown={handleKeyDown}
                        onBlur={handleBlur}
                    />
                )
            } else {
                return <Fragment>{formatValue(getValue())}</Fragment>
            }
        }
    }

    return (
        <Fragment>
            <td
                className={getClasses()}
                id={getId()}
                onDoubleClick={ () => {
                    if (isSelected()) {
                        dispatch(
                            SET_EDITING_CELL({
                                "cellId": cellId
                            })
                        );
                    }
                }}
            >
                {getCellContent()}
            </td>
        </Fragment>
    );
}

const comparisonFn = function(prevProps, nextProps) {
    return (
        prevProps.sheetUpdating === nextProps.sheetUpdating
    )
};

export default memo(MyHRTableCell, comparisonFn);
