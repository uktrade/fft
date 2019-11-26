import React, {Fragment, useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { SET_EDITING_CELL } from '../../Reducers/Edit'


const TableCell = ({cell, isHidden}) => {
    const dispatch = useDispatch();

    const [value, setValue] = useState(cell.value);
    const editCellId = useSelector(state => state.edit.cellId);

    const selectedRow = useSelector(state => state.selected.selectedRow);
    const allSelected = useSelector(state => state.selected.all);

    const isSelected = () => {
        if (allSelected) {
            return true
        }

        return selectedRow === cell.rowIndex
    }

    const getClasses = () => {
        let hiddenResult = '';
        let editable = '';

        if (isHidden) {
            hiddenResult = isHidden(cell.key) ? ' hidden' : ''
        }

        if (!cell.editable) {
            editable = ' not-editable';
        }

        return "govuk-table__cell " + (isSelected() ? 'selected' : '') + hiddenResult + editable
    }

    const handleKeyPress = (event) => {
        if(event.key === 'Enter'){
            dispatch(
                SET_EDITING_CELL({
                    "cellId": null
                })
            );
        }
    }

    const setContentState = (value) => {
        if (!parseInt(value)) {
            return
        }

        setValue(value)
    }

    return (
        <Fragment>
            <td
                className={getClasses()}

                onDoubleClick={ () => {
                    if (cell.isEditable) {
                        dispatch(
                            SET_EDITING_CELL({
                                "cellId": cell.id
                            })
                        );
                    }
                }}

                onMouseOver={ () => {
                    console.log(value)

                }}

                onMouseUp={ () => {

                }}
            >
                {editCellId === cell.id ? (
                    <input
                        className="cell-input"
                        type="text"
                        value={value}
                        onChange={e => setContentState(e.target.value)}
                        onKeyPress={handleKeyPress}
                    />
                ) : (
                    <Fragment>
                        {value}
                    </Fragment>
                )}
            </td>
        </Fragment>
    );
}

export default TableCell
