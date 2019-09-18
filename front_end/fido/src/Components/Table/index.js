import React, {Fragment, useState, useEffect, useRef } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';

import TableRow from '../../Components/TableRow/index'
import TableCell from '../../Components/TableCell/index'
import TableHandle from '../../Components/TableHandle/index'
import ColumnHeader from '../../Components/ColumnHeader/index'
import { SET_MOUSE_DOWN } from '../../Reducers/Mouse'
import { 
    SET_EDIT_CELL
} from '../../Reducers/Edit'
import {
    ADD_CELL,
    SELECT_CELL,
    UNSELECT_CELL,
    UNSELECT_ALL,
} from '../../Reducers/Cells'
import {
    getCellId
} from '../../Util'

function Table() {
    const LEFT_TO_RIGHT = 'LEFT_TO_RIGHT';
    const RIGHT_TO_LEFT = 'RIGHT_TO_LEFT';

    const TOP_TO_BOTTOM = 'TOP_TO_BOTTOM';
    const BOTTOM_TO_TOP = 'BOTTOM_TO_TOP';

    const dispatch = useDispatch();
    const initialCell = useSelector(state => state.select.initial);
    const lastCell = useSelector(state => state.select.last);

    // const selectedCells = useSelector(state => state.selection.cells);
    //const allCells = useSelector(state => state.allCells);
    // const isSelecting = useSelector(state => state.selection.isSelecting);

    const mouseDown = useSelector(state => state.mouse.down);
    const allCells = useSelector(state => state.allCells);

    //const [tableData, setTableData] = useState([]);

    const captureMouseDn = (e) => {
        dispatch({
            type: UNSELECT_ALL
        });

        if (e.srcElement.localName != "input") {
            dispatch({
                type: SET_EDIT_CELL,
                cellId: null
            });
        }

        dispatch({
            type: UNSELECT_ALL
        });

        dispatch({
            type: SET_MOUSE_DOWN,
            down: true
        });
    }

    const captureMouseUp = (e) => {
        dispatch({
            type: SET_MOUSE_DOWN,
            down: false
        });
    }

    useEffect(() => {
        window.table_data.forEach(function (cellData, rowIndex) {
            for (let key in cellData) {
                dispatch(
                    ADD_CELL({
                        id: getCellId(key, rowIndex),
                        rowIndex: rowIndex,
                        key: key,
                        value: cellData[key]
                    })
                );
            }
        });

        window.addEventListener("mousedown", captureMouseDn);
        window.addEventListener("mouseup", captureMouseUp);

        return () => {
            window.removeEventListener("onmouseup", captureMouseDn);
            window.removeEventListener("mousedown", captureMouseUp);
        };
    }, []);

	if (mouseDown) {
		let initial = allCells[initialCell];
		let last = allCells[lastCell];

        console.log(initial);
        console.log(last);

		if (initial && last) {

            let horizontalDirection = LEFT_TO_RIGHT;
            let verticalDirection = TOP_TO_BOTTOM;

            // Check for select direction
            if (initial.rect.x > last.rect.x) {
                // left to right
                horizontalDirection = RIGHT_TO_LEFT;
            }

            if (initial.rect.y > last.rect.y) {
                // top to bottom
                verticalDirection = BOTTOM_TO_TOP
            }

			for (let cellId in allCells) {
                let cell = allCells[cellId];

                if (!cell|| !cell.rect) {
                    break;
                }

                // console.log("cell", cell);

                let selectable = false;
				//let cell = allCells["id_" + selected];

                if (horizontalDirection === LEFT_TO_RIGHT) {
                    if (verticalDirection === TOP_TO_BOTTOM) {
                        if (
                            cell.rect.x <= last.rect.x &&
                            cell.rect.x >= initial.rect.x &&

                            cell.rect.y >= initial.rect.y &&
                            cell.rect.y <= last.rect.y
                        ) {
                            selectable = true;
                        }
                    } else {
                        if (
                            cell.rect.x <= last.rect.x &&
                            cell.rect.x >= initial.rect.x &&

                            cell.rect.y <= initial.rect.y &&
                            cell.rect.y >= last.rect.y
                        ) {
                            selectable = true;
                        }
                    }
                } else { // RIGHT_TO_LEFT
                    if (verticalDirection === TOP_TO_BOTTOM) {
                        if (
                            cell.rect.x >= last.rect.x &&
                            cell.rect.x <= initial.rect.x &&

                            cell.rect.y >= initial.rect.y &&
                            cell.rect.y <= last.rect.y
                        ) {
                            selectable = true;
                        }
                    } else {
                        if ( // BOTTOM_TO_TOP
                            cell.rect.x >= last.rect.x &&
                            cell.rect.x <= initial.rect.x &&

                            cell.rect.y <= initial.rect.y &&
                            cell.rect.y >= last.rect.y
                        ) {
                            selectable = true;
                        }
                    }
                }

                if (selectable) {
                    dispatch(
                        SELECT_CELL({
                            id: cellId
                        })
                    );
                } else {
                   dispatch(
                        UNSELECT_CELL({
                            id: cell.id
                        })
                    );
                }
			}
		}
	}

    const getCells = () => {
	    let cells = [];

	    let id = 0;

        if (window.table_data) {
            window.table_data.forEach(function (cellData, i) {
                cells.push(
                    <TableRow key={i} index={(i + 1)}>
                        <TableHandle rowIndex={i} />
                        <TableCell rowIndex={i} colIndex="0" cellId={getCellId("programme__programme_code", i)}>{cellData["programme__programme_code"]} - {cellData["programme__programme_description"]}</TableCell>
                        <TableCell rowIndex={i} colIndex="1" cellId={getCellId("apr", i)}>{cellData["apr"]}</TableCell>
                        <TableCell rowIndex={i} colIndex="2" cellId={getCellId("may", i)}>{cellData["may"]}</TableCell>
                        <TableCell rowIndex={i} colIndex="3" cellId={getCellId("jun", i)}>{cellData["jun"]}</TableCell>
                        <TableCell rowIndex={i} colIndex="3" cellId={getCellId("jul", i)}>{cellData["jul"]}</TableCell>
                        <TableCell rowIndex={i} colIndex="3" cellId={getCellId("aug", i)}>{cellData["aug"]}</TableCell>
                        <TableCell rowIndex={i} colIndex="3" cellId={getCellId("sep", i)}>{cellData["sep"]}</TableCell>
                    </TableRow>
                );
                id += 7;
            });
        }

	    return cells;
    }

    return (
        <table>
            <tbody>
                <TableRow index="0">
                    <th className="handle"></th>
                    <ColumnHeader index="0">Programme</ColumnHeader>
                    <ColumnHeader index="1">Apr</ColumnHeader>
                    <ColumnHeader index="2">May</ColumnHeader>
                    <ColumnHeader index="3">Jun</ColumnHeader>
                    <ColumnHeader index="4">Jul</ColumnHeader>
                    <ColumnHeader index="5">Aug</ColumnHeader>
                    <ColumnHeader index="6">Sep</ColumnHeader>
                </TableRow>
                {getCells()}
            </tbody>
        </table>
    );
}

export default Table;
