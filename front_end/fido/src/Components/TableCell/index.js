import React, {Fragment, useState, useEffect, useRef, useContext } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import {
    SET_INITIAL_CELL,
    SET_LAST_CELL,
    ADD_SELECTED_CELL
} from '../../Reducers/Selection'
import { 
    ADD_CELL,
    SET_EDITING,
    UNHIGHLIGHT_ALL,
    UNHIGHLIGHT_CELL
} from '../../Reducers/Cells'
import { 
    SET_EDIT_CELL
} from '../../Reducers/Edit'

function TableCell({children, cellId, rowIndex, colIndex}) {
    const dispatch = useDispatch();

    const [cellContent, setCellContent] = useState("test");

    let cellRef = React.createRef();
    const inputRef = useRef(null);

    const selectedCells = useSelector(state => state.selection.cells);
    const intialCell = useSelector(state => state.selection.intialCell);

    const mouseDn = useSelector(state => state.mouse.down);
    const allCells = useSelector(state => state.allCells);
    const editCell = useSelector(state => state.editCell.cellId);

    const selectCell = () => {
        if (mouseDn) {
            // dispatch({
            //     type: ADD_SELECTED_CELL,
            //     cell: cellId
            // });

            dispatch({
                type: SET_LAST_CELL,
                cell: cellId
            });
        }
    }

    useEffect(() => {
        dispatch(
            ADD_CELL({
                id: "id_" + cellId,
                rowIndex: rowIndex,
                colIndex: colIndex,
                rect: cellRef.current.getBoundingClientRect()
            })
        );
    }, []);

    useEffect(() => {
        if (inputRef && inputRef.current) {
            inputRef.current.focus();
        }
    });

    const isSelected = () => {
        let cellData = allCells["id_" + cellId];
        if (cellData && cellData.highlight) {
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
                    dispatch({
                        type: SET_INITIAL_CELL,
                        cell: cellId
                    });
                    dispatch({
                        type: SET_LAST_CELL,
                        cell: cellId
                    });
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
