import React, {Fragment, useState, useEffect, useRef, useContext } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import {
    SET_RECT,
    SELECT_CELL
} from '../../Reducers/Cells'
import { 
    SET_EDIT_CELL
} from '../../Reducers/Edit'
import {
    SET_INITIAL_CELL,
    SET_LAST_CELL
} from '../../Reducers/Select'
import {
    getCellId
} from '../../Util'

function TableCell({children, cellId}) {
    const dispatch = useDispatch();

    const [cellContent, setCellContent] = useState(children);

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

        //console.log("cellData", cellData);

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

    return (
        <Fragment>
            <td
                className={isSelected() ? 'highlight' : 'no-select'}
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
                        ref={inputRef}
                        type="text"
                        value={cellContent}
                        onChange={e => setCellContent(e.target.value)}
                        onKeyPress={handleKeyPress}
                    />
                ) : (
                    <Fragment>
                        {cellContent}
                    </Fragment>
                )}
            </td>
        </Fragment>
    );
}

export default TableCell;
