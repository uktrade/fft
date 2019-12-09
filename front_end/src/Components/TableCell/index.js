import React, {Fragment, useState, useEffect, useRef } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { SET_EDITING_CELL } from '../../Reducers/Edit'


const TableCell = ({isHidden, rowIndex, cellKey}) => {
    const dispatch = useDispatch();

    const cell = useSelector(state => state.allCells.cells[rowIndex][cellKey]);

    let wasEdited = false

    if (
        cell.versions &&
        cell.versions[cell.versions.length - 1].version > 1 &&
        cell.versions[cell.versions.length - 1].amount != cell.versions[0].amount
    ) {
        wasEdited = true
    }

    const [edited, setEdited] = useState(wasEdited);

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
        let hiddenResult = ''
        let editable = ''

        if (isHidden) {
            hiddenResult = isHidden(cellKey) ? ' hidden' : ''
        }

        if (!cell.editable) {
            editable = ' not-editable';
        }

        return "govuk-table__cell " + (edited ? 'edited ' : '') + (isSelected() ? 'selected' : '') + hiddenResult + editable
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

        console.log(value)
    }

    const isMounted = useRef(false);
    useEffect(() => {
        if (isMounted.current) {
            setEdited(true)
        }

        if (cell.value) {
            isMounted.current = true;
        }
    }, [cell.value]);

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

                onMouseOver={ () => {
                    //console.log(value)

                }}

                onMouseUp={ () => {

                }}
            >
                {editCellId === cell.id ? (
                    <input
                        className="cell-input"
                        type="text"
                        value={cell.value}
                        onChange={e => setContentState(e.target.value)}
                        onKeyPress={handleKeyPress}
                    />
                ) : (
                    <Fragment>
                        {cell.versions ? (
                            <Fragment>{cell.versions[0].amount}</Fragment>
                        ) : (
                            <Fragment>{cell.value}</Fragment>
                        )}
                    </Fragment>
                )}
            </td>
        </Fragment>
    );
}

export default TableCell
