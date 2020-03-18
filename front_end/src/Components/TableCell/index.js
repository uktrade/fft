import React, {Fragment, useState, useEffect, memo } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { SET_EDITING_CELL } from '../../Reducers/Edit'
import {
    postData,
    processForecastData,
    formatValue
} from '../../Util'
import { SET_ERROR } from '../../Reducers/Error'
import { SET_CELLS } from '../../Reducers/Cells'

const TableCell = ({rowIndex, cellId, cellKey, sheetUpdating}) => {

    let editing = false

    const checkValue = (val) => {
        if (cellId === val) {
            editing = true
            return false
        } else if (editing) {
            // Turn off editing
            editing = false
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

    const dispatch = useDispatch();

    const cells = useSelector(state => state.allCells.cells);
    const cell = useSelector(state => state.allCells.cells[rowIndex][cellKey]);
    const editCellId = useSelector(state => state.edit.cellId, checkValue);

    const [isUpdating, setIsUpdating] = useState(false)

    const selectedRow = useSelector(state => state.selected.selectedRow, checkSelectRow);
    const allSelected = useSelector(state => state.selected.all);

    let isEditable = true

    // Check for actual
    if (window.actuals.indexOf(cellKey) > -1) {
        isEditable = false
    }

    const getValue = () => {
        if (cell && cell.amount) {
            return (cell.amount / 100).toFixed(2)
        } else {
            return "0.00"
        }
    }

    const [value, setValue] = useState(getValue())

    useEffect(() => {
        if (cell) {
            setValue((cell.amount / 100).toFixed(2))
        }
    }, [cell]);

    const isSelected = () => {
        if (allSelected) {
            return true
        }

        return selectedRow === rowIndex
    }

    const wasEdited = () => {
        if (!isEditable)
            return false

        return cell.amount !== cell.startingAmount
    }

    const getClasses = () => {
        let editable = ''

        if (!isEditable) {
            editable = ' not-editable'
        }

        if (!cell)
            return "govuk-table__cell forecast-month-cell figure-cell " + (isSelected() ? 'selected' : '') + editable

        let negative = ''

        if (cell.amount < 0) {
            negative = " negative"
        }

        return "govuk-table__cell forecast-month-cell figure-cell " + (wasEdited() ? 'edited ' : '') + (isSelected() ? 'selected' : '')  + editable + negative
    }

    const setContentState = (value) => {
        var re = /^-?\d*\.?\d{0,12}$/; 
        var isValid = (value.match(re) !== null);

        if (!isValid) {
            return
        }
        setValue(value)
    }


    const updateValue = () => {
        let newAmount = value * 100

        if (newAmount > Number.MAX_SAFE_INTEGER) {
            newAmount = Number.MAX_SAFE_INTEGER
        }

        if (newAmount < Number.MIN_SAFE_INTEGER) {
            newAmount = Number.MIN_SAFE_INTEGER
        }

        let intAmount = parseInt(newAmount)

        if (cell && intAmount === cell.amount) {
            return
        }

        if (!cell && intAmount === 0) {
            return
        }

        setIsUpdating(true)

        let crsfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value

        let payload = new FormData()
        payload.append("natural_account_code", cells[rowIndex]["natural_account_code"].value)
        payload.append("programme_code", cells[rowIndex]["programme"].value)
        payload.append("project_code", cells[rowIndex]["project_code"].value)
        payload.append("analysis1_code", cells[rowIndex]["analysis1_code"].value)
        payload.append("analysis2_code", cells[rowIndex]["analysis2_code"].value)
        payload.append("csrfmiddlewaretoken", crsfToken)
        payload.append("month", cellKey)
        payload.append("amount", intAmount)

        postData(
            `/forecast/update-forecast/${window.cost_centre}/`,
            payload
        ).then((response) => {
            setIsUpdating(false)
            if (response.status === 200) {
                let rows = processForecastData(response.data)
                  dispatch({
                    type: SET_CELLS,
                    cells: rows
                  })
            } else {
                dispatch(
                    SET_ERROR({
                        errorMessage: response.data.error
                    })
                );
            }
        })
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
                    if (isEditable) {
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

export default memo(TableCell, comparisonFn);
