import React, {Fragment } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import { SET_EDITING_CELL } from '../../Reducers/Edit'


const TableCell = ({isHidden, rowIndex, cellKey}) => {
    const dispatch = useDispatch();

    const cell = useSelector(state => state.allCells.cells[rowIndex][cellKey]);

    const editCellId = useSelector(state => state.edit.cellId);

    const selectedRow = useSelector(state => state.selected.selectedRow);
    const allSelected = useSelector(state => state.selected.all);

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

    const formatValue = (value) => {
        let nfObject = new Intl.NumberFormat('en-GB'); 
        let pounds = Math.round(value / 100)
        return nfObject.format(pounds); 
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
                            <Fragment>{formatValue(cell.versions[0].amount)}
                            </Fragment>
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
