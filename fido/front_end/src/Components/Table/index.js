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
    getCellId,
    months
} from '../../Util'
import {
    SET_INITIAL_CELL,
    SET_LAST_CELL
} from '../../Reducers/Select'

function Table() {
    const LEFT_TO_RIGHT = 'LEFT_TO_RIGHT';
    const RIGHT_TO_LEFT = 'RIGHT_TO_LEFT';

    const TOP_TO_BOTTOM = 'TOP_TO_BOTTOM';
    const BOTTOM_TO_TOP = 'BOTTOM_TO_TOP';

    const dispatch = useDispatch();
    const initialCell = useSelector(state => state.select.initial);
    const lastCell = useSelector(state => state.select.last);

    const [allCellsArr, setAllCellsArr] = useState([]);
    const [errorMessage, setErrorMessage] = useState(null);

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

    const handleKeyDown = (event) => {
        console.log(event);
        if (event.keyCode == 9 && event.target.localName != "input") {            
            const state = store.getState();
            // Get next cell
            let cellData =  state.allCells[state.select.initial]
            let colIndex = months.indexOf(cellData.key);

            let inScope = [];

            // TODO - do this once at the start of the app
            for (const key in state.allCells) {
                let cell = state.allCells[key];
                inScope.push(cell);
            }

            console.log(inScope);

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

    const getTopLeftCell = (cells, initialCell) => {
        let topLeftCell = initialCell;

        for (const cell of cells) {
            if (cell.rect.x < topLeftCell.rect.x && 
                cell.rect.y < topLeftCell.rect.y) {
                topLeftCell = cell
            }
        }

        return topLeftCell
    }

    const capturePaste = (e) => {
        let pasteContent = e.clipboardData.getData('Text');
        let lines = pasteContent.split('\n');
        const state = store.getState();

        let initial = state.select.initial;
        let initialCell = state.allCells[initial];

        let inScope = [];
        // TODO - do this once at the start of the app
        for (const key in state.allCells) {
            let cell = state.allCells[key];
            inScope.push(cell);
        }

        if (!initialCell.selected) {
            return
        }

        let selectedCells = inScope.filter((cell) => {
            return cell.selected
        });

        // Find top left cell
        let topLeftCell = getTopLeftCell(selectedCells, initialCell)
        let rowIndex = topLeftCell.rowIndex

        for (const line of lines) {
            let lineParts = line.split('\t')
            let colIndex = months.indexOf(topLeftCell.key);

            for (const linePart of lineParts) {
                if (!parseInt(linePart)) {
                    setErrorMessage("You can only paste whole numbers into cells");
                    continue
                }

                let cells = inScope.filter((cell) => {
                    return (
                        cell.rowIndex == rowIndex &&
                        cell.key === months[colIndex]
                    )
                })
                if (cells[0]) {
                    dispatch(
                        SET_VALUE({
                            id: cells[0].id,
                            value: linePart
                        })
                    );

                    dispatch(
                        SELECT_CELL({
                            id: cells[0].id
                        })
                    );

                    dispatch(
                        SET_LAST_CELL({
                            id: cells[0].id
                        })
                    )
                }

                colIndex++
            }
            rowIndex++
        }
    }

    const setClipBoardContent = (e) => {

        const state = store.getState();
        // TODO - do this once at the start of the app
        let inScope = [];
        for (const key in state.allCells) {
            let cell = state.allCells[key];
            inScope.push(cell);
        }

        let initial = state.select.initial;
        let initialCell = state.allCells[initial];

        if (!initialCell.selected) {
            return
        }

        e.preventDefault();

        let selectedCells = inScope.filter((cell) => {
            return cell.selected
        });

        let topLeftCell = getTopLeftCell(selectedCells, initialCell)

        console.log(selectedCells);

        let clipBoardContent = "";

        // let currentRow = topLeftCell.rowIndex

        let rowIndex = topLeftCell.rowIndex

        for (const cell of selectedCells) {
            if (cell.rowIndex != rowIndex) {
                rowIndex = cell.rowIndex
                clipBoardContent += "\n"
            }
            clipBoardContent += cell.value + "\t"

            console.log(cell.value + "\t");
            console.log(clipBoardContent);
        }

        console.log("clipBoardContent.trim()", clipBoardContent);

        navigator.clipboard.writeText(clipBoardContent)
    }

    useEffect(() => {
        window.cell_data = allCells;
    }, [allCells]);

    useEffect(() => {
        let cellIndex = 0;
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
                        index: cellIndex,
                        rowIndex: rowIndex,
                        key: key,
                        value: cellData[key],
                        editable: editable,
                        programmeCode: cellData["programme__programme_code"],
                        naturalAccountCode: cellData["natural_account_code__natural_account_code"]
                    })
                );
                cellIndex++;
            }
        });

        window.addEventListener("mousedown", captureMouseDn);
        window.addEventListener("mouseup", captureMouseUp);
        window.addEventListener("paste", capturePaste);
        window.addEventListener("keydown", handleKeyDown);
        window.addEventListener("copy", setClipBoardContent);

        return () => {
            window.removeEventListener("onmouseup", captureMouseDn);
            window.removeEventListener("mousedown", captureMouseUp);
            window.removeEventListener("paste", capturePaste);
            window.removeEventListener("keydown", handleKeyDown);
            window.removeEventListener("copy", setClipBoardContent);
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
            let cellIndex = 0;
            window.table_data.forEach(function (cellData, i) {
                let monthCells = [];
                for (const month of months) {
                    let id = getCellId(month, i)
                    monthCells.push(
                        <TableCell key={cellIndex} index={cellIndex} cellId={id} />
                    )
                    cellIndex++
                }
                cells.push(
                    <TableRow key={i} index={(i + 1)}>
                        <TableHandle rowIndex={i}>{cellData["programme__programme_code"]} - {cellData["programme__programme_description"]}</TableHandle>
                        {monthCells}
                    </TableRow>
                );
            });
        }
	    return cells;
    }

    return (
        <Fragment>
            {errorMessage &&
                <div className="govuk-error-summary" aria-labelledby="error-summary-title" role="alert" tabIndex="-1" data-module="govuk-error-summary">
                    <h2 className="govuk-error-summary__title" id="error-summary-title">
                        There is a problem
                    </h2>
                    <div className="govuk-error-summary__body">
                        <ul className="govuk-list govuk-error-summary__list">
                            <li>
                                <a href="#passport-issued-error">{errorMessage}</a>
                            </li>
                        </ul>
                    </div>
                </div>
            }
            <table className="govuk-table" id="forecast-table">
                <caption className="govuk-table__caption">Edit forecast</caption>
                <thead className="govuk-table__head">
                    <TableRow index="0">
                        <ColumnHeader colKey="programme__programme_code">Programme</ColumnHeader>
                        <ColumnHeader colKey="apr">Apr</ColumnHeader>
                        <ColumnHeader colKey="may">May</ColumnHeader>
                        <ColumnHeader colKey="jun">Jun</ColumnHeader>
                        <ColumnHeader colKey="jul">Jul</ColumnHeader>
                        <ColumnHeader colKey="aug">Aug</ColumnHeader>
                        <ColumnHeader colKey="sep">Sep</ColumnHeader>
                        <ColumnHeader colKey="oct">Oct</ColumnHeader>
                        <ColumnHeader colKey="nov">Nov</ColumnHeader>
                        <ColumnHeader colKey="dec">Dec</ColumnHeader>
                        <ColumnHeader colKey="jan">Jan</ColumnHeader>
                        <ColumnHeader colKey="feb">Feb</ColumnHeader>
                        <ColumnHeader colKey="mar">Mar</ColumnHeader>
                    </TableRow>
                </thead>
                <tbody className="govuk-table__body">
                    {getCells()}
                </tbody>
            </table>
        </Fragment>
    );
}

export default Table;
