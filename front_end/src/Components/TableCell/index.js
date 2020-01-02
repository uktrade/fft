import React, {Fragment, useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { SET_EDITING_CELL } from '../../Reducers/Edit'
import {
    postData,
    processForecastData
} from '../../Util'
import { SET_ERROR } from '../../Reducers/Error'
import { SET_CELLS } from '../../Reducers/Cells'

const TableCell = ({isHidden, rowIndex, cellKey}) => {
    const dispatch = useDispatch();

    const cells = useSelector(state => state.allCells.cells);
    const cell = useSelector(state => state.allCells.cells[rowIndex][cellKey]);
    const editCellId = useSelector(state => state.edit.cellId);

    const [isUpdating, setIsUpdating] = useState(false)

    const selectedRow = useSelector(state => state.selected.selectedRow);
    const allSelected = useSelector(state => state.selected.all);

    let initialValue = null

    if (cell.versions && cell.versions.length > 0) {
        initialValue = cell.versions[0].amount
    }

    const [editValue, setEditValue] = useState((initialValue/100).toFixed(2))

    const isSelected = () => {
        if (allSelected) {
            return true
        }

        return selectedRow === cell.rowIndex
    }

    const wasEdited = () => {
        // TODO - add function after "previous months" story
        return false
    }

    const getClasses = () => {
        let hiddenResult = ''
        let editable = ''
        let negative = ''

        if (isHidden) {
            hiddenResult = isHidden(cellKey) ? ' hidden' : ''
        }

        if (!cell.isEditable) {
            editable = ' not-editable';
        }

        if (cell.versions && cell.versions[0].amount < 0) {
            negative = " negative"
        }

        return "govuk-table__cell forecast-month-cell " + (wasEdited() ? 'edited ' : '') + (isSelected() ? 'selected' : '') + hiddenResult + editable + negative
    }

    const setContentState = (value) => {
        var re = /^-?\d*\.?\d{0,12}$/; 
        var isValid = (value.match(re) !== null);

        if (!isValid) {
            return
        }
        setEditValue(value)
    }

    const formatValue = (value) => {
        let nfObject = new Intl.NumberFormat('en-GB'); 
        let pounds = Math.round(value / 100)
        return nfObject.format(pounds); 
    }

    const updateValue = () => {
        let newAmount = parseInt(editValue * 100)

        if (newAmount === cell.versions[0].amount) {
            return
        }

        setIsUpdating(true)

        let payload = new FormData()

        payload.append("natural_account_code", cells[rowIndex]["natural_account_code"].value)
        payload.append("programme_code", cells[rowIndex]["programme"].value)
        payload.append("project_code", cells[rowIndex]["project_code"].value)
        payload.append("analysis1_code", cells[rowIndex]["analysis1_code"].value)
        payload.append("analysis2_code", cells[rowIndex]["analysis2_code"].value)

        payload.append("month", cell.key)
        payload.append("amount", newAmount)

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
    }

    const handleKeyDown = (event) => {
        if (event.key === "Tab") {
            updateValue()
        }
    }

    const handleKeyPress = (event) => {
        if(event.key === 'Enter') {
            updateValue()
            dispatch(
                SET_EDITING_CELL({
                    "cellId": null
                })
            );

            event.preventDefault()
        }
    }

    return (
        <Fragment>
            <td
                className={getClasses()}
                id={cell.id}
                onDoubleClick={ () => {
                    if (cell.isEditable) {
                        dispatch(
                            SET_EDITING_CELL({
                                "cellId": cell.id
                            })
                        );
                    }
                }}
            >
                {isUpdating ? (
                    <Fragment>
                        UPDATING...
                    </Fragment>
                ) : (
                    <Fragment>
                        {editCellId === cell.id ? (
                            <input
                                id={cell.id + "_input"}
                                className="cell-input"
                                type="text"
                                value={editValue}
                                onChange={e => setContentState(e.target.value)}
                                onKeyPress={handleKeyPress}
                                onKeyDown={handleKeyDown}
                                onBlur={handleBlur}
                            />
                        ) : (
                            <Fragment>
                                {cell.versions && cell.versions.length > 0 ? (
                                    <Fragment>{formatValue(cell.versions[0].amount)}</Fragment>
                                ) : (
                                    <Fragment>{cell.value}</Fragment>
                                )}
                            </Fragment>
                        )}
                    </Fragment>
                )}
            </td>
        </Fragment>
    );
}

export default TableCell
