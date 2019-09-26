import React, {Fragment, useState, useEffect, useRef, useContext } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import {
    SET_RECT,
    SELECT_CELL,
    SET_VALUE,
    UNSELECT_ALL
} from '../../Reducers/Cells'
import { 
    SET_EDIT_CELL
} from '../../Reducers/Edit'
import {
    SET_INITIAL_CELL,
    SET_LAST_CELL
} from '../../Reducers/Select'
import {
    getCellId,
    months
} from '../../Util'

function TableCell({children, index, cellId}) {
    const dispatch = useDispatch();

    let cellRef = React.createRef();
    const inputRef = useRef(null);

    const mouseDn = useSelector(state => state.mouse.down);
    const allCells = useSelector(state => state.allCells);
    const editCell = useSelector(state => state.editCell.cellId);

    const selectCell = () => {
        if (mouseDn) {
            dispatch(
                SELECT_CELL({
                    id: cellId
                })
            );

            dispatch(
                SET_LAST_CELL({
                    id: cellId
                })
            );
        }
    }

    useEffect(() => {
        if (allCells) {
            dispatch(
                SET_RECT({
                    id: cellId,
                    rect: cellRef.current.getBoundingClientRect()
                })
            );
        }
    }, []);

    useEffect(() => {
        if (inputRef && inputRef.current) {
            inputRef.current.focus();
        }
    });

    const isSelected = () => {
        let cellData = allCells[cellId];

        if (cellData && cellData.selected) {
            return true;
        }

        return false
    }

    const handleKeyPress = (event) => {
        if(event.key === 'Enter'){
            dispatch({
                type: SET_EDIT_CELL,
                cellId: null
            });
        }
    }

    const handleKeyDown = (event) => {
        if (event.keyCode == 9) {
            // Get next cell
            let cellData = allCells[cellId]
            let colIndex = months.indexOf(cellData.key);

            let inScope = [];

            // TODO - do this once at the start of the app
            for (const key in allCells) {
                let cell = allCells[key];
                inScope.push(cell);
            }

            let cells = inScope.filter((cell) => {
                return (
                    cell.rowIndex == cellData.rowIndex &&
                    cell.key === months[colIndex + 1]
                )
            })

            let nextCell = cells[0]

            dispatch({
                type: UNSELECT_ALL
            });

            dispatch(
                SET_LAST_CELL({
                    id: nextCell.id
                })
            );

            dispatch(
                SET_INITIAL_CELL({
                    id: nextCell.id
                })
            );

            dispatch(
                SELECT_CELL({
                    id: nextCell.id
                })
            );

            dispatch({
                type: SET_EDIT_CELL,
                cellId: nextCell.id
            });
        }
    }

    const setContentState = (value) => {
        //setCellContent(value);
        if (!parseInt(value)) {
            return
        }

        dispatch(
            SET_VALUE({
                id: cellId,
                value: value
            })
        );
    }

    return (
        <Fragment>
            <td
                className={isSelected() ? 'highlight govuk-table__cell' : 'no-select govuk-table__cell'}
                ref={cellRef}
                onDoubleClick={ () => {
                    dispatch({
                        type: SET_EDIT_CELL,
                        cellId: cellId
                    });
                }}

                onMouseOver={ () => { 
                    selectCell();
                }}

                onMouseDown={ () => {
                    dispatch(
                        SELECT_CELL({
                            id: cellId
                        })
                    );

                    dispatch(
                        SET_INITIAL_CELL({
                            id: cellId
                        })
                    );

                    dispatch(
                        SET_LAST_CELL({
                            id: cellId
                        })
                    );
                }}
            >
                {editCell == cellId ? (
                    <input
                        className="cell-input"
                        ref={inputRef}
                        type="text"
                        value={allCells[cellId].value}
                        onChange={e => setContentState(e.target.value)}
                        onKeyPress={handleKeyPress}
                        onKeyDown={handleKeyDown}
                    />
                ) : (
                    <Fragment>
                        {allCells[cellId].value}
                    </Fragment>
                )}
            </td>
        </Fragment>
    );
}

export default TableCell;
