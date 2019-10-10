import React, {Fragment, useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import update from 'react-addons-update';

import { store } from '../../Store';

import TableRow from '../../Components/TableRow/index'
import TableCell from '../../Components/TableCell/index'
import TableHandle from '../../Components/TableHandle/index'
import ColumnHeader from '../../Components/ColumnHeader/index'

import {
    getCellId,
    months
} from '../../Util'

/* TODO
List of selected cells
Pasting
Copying
Cut down cell loop to relevant cells
*/

function Table({rowData, cellCount}) {
    const dispatch = useDispatch();

    const LEFT_TO_RIGHT = 'LEFT_TO_RIGHT';
    const RIGHT_TO_LEFT = 'RIGHT_TO_LEFT';

    const TOP_TO_BOTTOM = 'TOP_TO_BOTTOM';
    const BOTTOM_TO_TOP = 'BOTTOM_TO_TOP';

    const [errorMessage, setErrorMessage] = useState(null);

    const mouseRef = useRef(false);
    const editCellRef = useRef(null)

    const rects = []

    const [rows, setRows] = useState([]);

    const selectedCellsRef = useRef([]);
    const [selectedCells, setSelectedCells] = useState([])

    const [initialSelection, setInitialSelection] = useState([])
    const [lastSelection, setlastSelection] = useState([])

    useEffect(() => {
        window.addEventListener("mousedown", captureMouseDn);
        window.addEventListener("mouseup", captureMouseUp);
        // window.addEventListener("paste", capturePaste);
        // window.addEventListener("keydown", handleKeyDown);
        // window.addEventListener("copy", setClipBoardContent);

        return () => {
           window.removeEventListener("onmouseup", captureMouseUp);
            window.removeEventListener("mousedown", captureMouseDn);
            // window.removeEventListener("paste", capturePaste);
            // window.removeEventListener("keydown", handleKeyDown);
            // window.removeEventListener("copy", setClipBoardContent);
        };


    }, []);

    useEffect(() => {
        console.log("Whoopppppp")

        console.log("rowData...", rowData)
        setRows(rowData)

    }, [rowData]);

    const updateRow = (cellId, row, property, value=true) => {
        let cellIndex = rows[row].findIndex(function(element) {
          return element.id === cellId
        });


        // TODO - reinstate after figuring out issue
        // let newRows = update(rows, {[row]: {
        //             [cellIndex]: {
        //                 [property]: {$set: value}
        //             }
        //         }
        //     }
        // )

        let newRows = [...rows];
        newRows[row][cellIndex][property] = value

        setRows(newRows);
    }

    const removeFromSelected = (arr, cellId) => {
        var index = arr.findIndex(cell => cell.id === cellId);
        if (index > -1) {
            arr.splice(index, 1);
        }

        return index
    }

    const mouseOverCell = (cellId, row, col) => {
        if (mouseRef.current) {
            setlastSelection({
                "id": cellId,
                "row": row,
                "col": col
            })
        }
    }

    const selectInitialCell = (cellId, row, col) => {
        let newRows = [...rows];

        if (editCellRef.current) {
            let cellIndex = getCellIndex(editCellRef.current.id, editCellRef.current.row)
            newRows[editCellRef.current.row][cellIndex]["editing"] = false
        }

        for (let selected of selectedCellsRef.current) {
            let cellIndex = getCellIndex(selected.id, selected.row)
            newRows[selected.row][cellIndex]["selected"] = false
        }

        let cellIndex = getCellIndex(cellId, row)
        newRows[row][cellIndex]["selected"] = true

        setRows(newRows);

        selectedCellsRef.current = [{
            "id": cellId,
            "row": row
        }]

        setInitialSelection({
            "id": cellId,
            "row": row,
            "col": col
        })

        setlastSelection({
            "id": cellId,
            "row": row,
            "col": col
        })
    }

    const mouseUpOnCell = (cellId, row, col) => {
        setlastSelection([cellId, row, col])
    }

    const editCell = (cellId, row) => {
        let newRows = [...rows];

        let cellIndex = getCellIndex(cellId, row)
        newRows[row][cellIndex]["editing"] = true

        editCellRef.current = {
            id: cellId,
            row: row
        }

        setRows(newRows)
    }

    const captureMouseUp = (e) => {
        mouseRef.current = false
    }

    const captureMouseDn = (e) => {
        mouseRef.current = true
    }

    const setRect = (cellId, row, rect) => {
        //console.log("Setitng rect...", cellCount, rects.length)

        rects.push(rect)

        if (cellCount === rects.length) {
            let newRows = [...rows];
            let rectCounter = 0

            newRows.forEach(function (row, i) {
                row.forEach(function (cellData, j) {
                    if (months.includes(cellData.key.toLowerCase())) {
                        newRows[i][j]["rect"] = rects[rectCounter]
                        rectCounter++
                    }
                })
            })

            setRows(newRows);
        }
    }

    const getCellData = (cellId, row) => {
        let index = getCellIndex(cellId, row)
        return rows[row][index]
    }

    const getCellIndex = (cellId, row) => {
        var cellIndex = rows[row].findIndex(function(element) {
          return element.id === cellId
        });

        return cellIndex
    }

    const createSelectionArea = () => {
        if (mouseRef.current && initialSelection && lastSelection) {
            let initial = getCellData(initialSelection.id, initialSelection.row)
            let last = getCellData(lastSelection.id, lastSelection.row)

            let newRows = [...rows]
            let changed = false

            let selected = [...selectedCells];

            if (initial.rect && last.rect) {
                for (let sel of selectedCellsRef.current) {
                    if (
                        sel.id != initialSelection.id &&
                        sel.id != lastSelection.id
                    ) {
                        let cellIndex = getCellIndex(sel.id, sel.row)
                        newRows[sel.row][cellIndex]["selected"] = false


                        // let newRows = update(rows, {[row]: {
                        //             [cellIndex]: {
                        //                 [property]: {$set: value}
                        //             }
                        //         }
                        //     }
                        // )


                    }
                }

                selectedCellsRef.current = [
                    initialSelection,
                    lastSelection
                ]

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

                let relevantRows = []
                let colStart = 0
                let colEnd = 0

                // Only look at cells in the same rows as inital and last
                //if (horizontalDirection === LEFT_TO_RIGHT) {
                if (verticalDirection === TOP_TO_BOTTOM) {
                    relevantRows = rows.filter((rowObj, index) => {
                        // Return element for new_array
                        return index >= initialSelection.row && index <= lastSelection.row
                    })
                } else {
                    relevantRows = rows.filter((rowObj, index) => {
                        // Return element for new_array
                        return index <= initialSelection.row && index >= lastSelection.row
                    })
                }

                if (horizontalDirection === LEFT_TO_RIGHT) {
                    colStart = initialSelection.col
                    colEnd = lastSelection.col
                } else {
                    colStart = lastSelection.col
                    colEnd = initialSelection.col
                }

                for (let row of relevantRows) {
                    for (let cell of row) {
                        if (!cell || !cell.rect) {
                            continue;
                        }

                        if (colStart != colEnd && (cell.colIndex < colStart || cell.colIndex > colEnd)) {
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

                        let cellIndex = getCellIndex(cell.id, cell.rowIndex)

                        if (selectable) {
                            let isSelected = newRows[cell.rowIndex][cellIndex]["selected"]

                            if (!isSelected) {
                                newRows[cell.rowIndex][cellIndex]["selected"] = true
                                selectedCellsRef.current.push({
                                    id: cell.id,
                                    row: cell.rowIndex
                                })
                                changed = true
                            }
                        } else {
                            newRows[cell.rowIndex][cellIndex]["selected"] = false
                            changed = removeFromSelected(selectedCellsRef.current, cell.id)
                        }
                    }
                }
            }

            if (changed) {
                 setRows(newRows);
            }
        }
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
            <table
                onMouseMove={createSelectionArea}
                onMouseDown={createSelectionArea}
                className="govuk-table" id="forecast-table">
                <caption className="govuk-table__caption">Edit forecast</caption>
                <thead className="govuk-table__head">
                    <TableRow index="0">
                        <th className="govuk-table__header ">Programme</th>
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
                    {rows.map((rowData, rowIndex) => {
                        //console.log("rowData from table...", rowData)
                        return <TableRow key={rowIndex} index={(rowIndex + 1)}>
                            <TableHandle rowIndex={rowIndex}>{
                                rowData["programme__programme_code"]} - {rowData["programme__programme_description"]}
                            </TableHandle>
                            {rowData.map((cell, cellIndex) => {
                                //console.log("cell key", cell.key.toLowerCase())

                                if (months.includes(cell.key.toLowerCase())) {
                                    return <TableCell
                                        row={rowIndex}
                                        col={cell.colIndex}
                                        key={cellIndex}
                                        index={cellIndex}
                                        cellId={cell.id}
                                        selected={cell.selected}
                                        editing={cell.editing}
                                        setEditing={editCell}
                                        selectInitialCell={selectInitialCell}
                                        initialValue={cell.value}
                                        mouseOverCell={mouseOverCell}
                                        mouseUpOnCell={mouseUpOnCell}
                                        setRect={setRect}
                                    />
                                }
                            })}
                        </TableRow>
                    })}
                </tbody>
            </table>
        </Fragment>
    );
}

export default Table;