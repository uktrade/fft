import React, {Fragment, useState, useEffect, useRef } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';

import { store } from '../../Store';

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
    SET_VALUE,
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

    const capturePaste = (e) => {
        let pasteContent = e.clipboardData.getData('Text');
        let lines = pasteContent.split('\n');
        const state = store.getState();

        for (let i = 0; i < lines.length; i++) {
            let line = lines[i];
            let values = line.split('\t');

            for (let j = 0; j < values.length; j++) {
                let newCellVal = values[j];

                for (let key in state.allCells) {
                    let cell = state.allCells[key];

                    if (cell.selected) {
                        dispatch(
                            SET_VALUE({
                                id: cell.id,
                                value: newCellVal
                            })
                        );
                    }
                }
            };
        };
    }

    useEffect(() => {
        window.cell_data = allCells;
    }, [allCells]);

    useEffect(() => {
        window.table_data.forEach(function (cellData, rowIndex) {
            for (let key in cellData) {

                let editable = false;

                for (let i = 0; i < window.editable_periods.length; i++) {
                    let shortName = window.editable_periods[i]["fields"]["period_short_name"];
                    if (shortName && shortName.toLowerCase() == key) {
                        editable = true;
                        break;
                    }
                }

                dispatch(
                    ADD_CELL({
                        id: getCellId(key, rowIndex),
                        rowIndex: rowIndex,
                        key: key,
                        value: cellData[key],
                        editable: editable,
                        programmeCode: cellData["programme__programme_code"],
                        naturalAccountCode: cellData["natural_account_code__natural_account_code"]
                    })
                );
            }
        });

        window.addEventListener("mousedown", captureMouseDn);
        window.addEventListener("mouseup", captureMouseUp);

        window.addEventListener("paste", capturePaste);

        return () => {
            window.removeEventListener("onmouseup", captureMouseDn);
            window.removeEventListener("mousedown", captureMouseUp);

            window.removeEventListener("paste", capturePaste);
        };
    }, []);

	if (mouseDown) {
		let initial = allCells[initialCell];
		let last = allCells[lastCell];

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

                if (!cell || !cell.rect) {
                    continue;
                }

                let selectable = false;

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
            });
        }

	    return cells;
    }

    return (
        <table>
            <tbody>
                <TableRow index="0">
                    <th className="handle"></th>
                    <ColumnHeader colKey="programme__programme_code">Programme</ColumnHeader>
                    <ColumnHeader colKey="apr">Apr</ColumnHeader>
                    <ColumnHeader colKey="may">May</ColumnHeader>
                    <ColumnHeader colKey="jun">Jun</ColumnHeader>
                    <ColumnHeader colKey="jul">Jul</ColumnHeader>
                    <ColumnHeader colKey="aug">Aug</ColumnHeader>
                    <ColumnHeader colKey="sep">Sep</ColumnHeader>
                </TableRow>
                {getCells()}
            </tbody>
        </table>
    );
}

export default Table;
