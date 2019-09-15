import React, {Fragment, useState, useEffect, useRef } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';

import TableRow from '../../Components/TableRow/index'
import TableCell from '../../Components/TableCell/index'
import TableHandle from '../../Components/TableHandle/index'
import ColumnHeader from '../../Components/ColumnHeader/index'
import { SET_MOUSE_DOWN } from '../../Reducers/Mouse'
import { 
    UNSELECT_ALL, 
    IS_SELECTING, 
    ADD_CELL_TO_SELECTION 
} from '../../Reducers/Selection'
import { 
    HIGHLIGHT_CELL, 
    UNHIGHLIGHT_CELL,
    UNHIGHLIGHT_ALL
} from '../../Reducers/Cells'
import { 
    SET_EDIT_CELL
} from '../../Reducers/Edit'

function Table() {
    const LEFT_TO_RIGHT = 'LEFT_TO_RIGHT';
    const RIGHT_TO_LEFT = 'RIGHT_TO_LEFT';

    const TOP_TO_BOTTOM = 'TOP_TO_BOTTOM';
    const BOTTOM_TO_TOP = 'BOTTOM_TO_TOP';

    const dispatch = useDispatch();
    const initialCell = useSelector(state => state.selection.initialCell);
    const lastCell = useSelector(state => state.selection.lastCell);
    const selectedCells = useSelector(state => state.selection.cells);
    const allCells = useSelector(state => state.allCells);
    const isSelecting = useSelector(state => state.selection.isSelecting);

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
            type: UNHIGHLIGHT_ALL
        });

        dispatch({
            type: SET_MOUSE_DOWN,
            down: true
        });

        dispatch({
            type: IS_SELECTING,
            isSelecting: true
        });
    }

    const captureMouseUp = (e) => {
        dispatch({
            type: SET_MOUSE_DOWN,
            down: false
        });

        dispatch({
            type: IS_SELECTING,
            isSelecting: false
        });
    }

    useEffect(() => {
        window.addEventListener("mousedown", captureMouseDn);
        window.addEventListener("mouseup", captureMouseUp);

        return () => {
            window.removeEventListener("onmouseup", captureMouseDn);
            window.removeEventListener("mousedown", captureMouseUp);
        };
    }, []);

	if (isSelecting) {
		let initial = allCells["id_" + initialCell];
		let last = allCells["id_" + lastCell];

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

                if (!cell) {
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
                        HIGHLIGHT_CELL({
                            id: cell.id
                        })
                    );

                   dispatch({
                        type: ADD_CELL_TO_SELECTION,
                        id: cell.id
                    });
                    
                } else {
                   dispatch(
                        UNHIGHLIGHT_CELL({
                            id: cell.id
                        })
                    );
                }

                //console.log("=====\\======");
			}
		}
	}

  //   const showBorder = () => {
    	
  //   	//console.log("allCells", allCells);

  //   	// Find first cell
  //   	// find bottom right
  //   	console.log(initialCell);

  //   	// let furthestDown = allCells["id_" + initialCell];
  //   	// let furthestRight = allCells["id_" + initialCell];

		// for (let selected of selectedCells) {
			
		// }
  //   }

    return (
        <table>
            <tbody>
                <TableRow index="0">
                    <th className="handle"></th>
                    <ColumnHeader index="0">Col 1</ColumnHeader>
                    <ColumnHeader index="1">Col 2</ColumnHeader>
                    <ColumnHeader index="2">Col 3</ColumnHeader>
                    <ColumnHeader index="3">Col 4</ColumnHeader>
                    <ColumnHeader index="4">Col 5</ColumnHeader>
                    <ColumnHeader index="5">Col 6</ColumnHeader>
                    <ColumnHeader index="6">Col 7</ColumnHeader>
                    <ColumnHeader index="7">Col 8</ColumnHeader>
                    <ColumnHeader index="8">Col 9</ColumnHeader>
                </TableRow>
            	<TableRow index="0">
                    <TableHandle rowIndex="0" />
            		<TableCell rowIndex="0" colIndex="0" cellId="1">This is a test...</TableCell>
                    <TableCell rowIndex="0" colIndex="1" cellId="2">This is a test...</TableCell>
                    <TableCell rowIndex="0" colIndex="2" cellId="3">This is a test...</TableCell>
                    <TableCell rowIndex="0" colIndex="3" cellId="4">This is a test...</TableCell>
                    <TableCell rowIndex="0" colIndex="4" cellId="5">This is a test...</TableCell>
                    <TableCell rowIndex="0" colIndex="5" cellId="6">This is a test...</TableCell>
                    <TableCell rowIndex="0" colIndex="6" cellId="7">This is a test...</TableCell>
                    <TableCell rowIndex="0" colIndex="7" cellId="8">This is a test...</TableCell>
                    <TableCell rowIndex="0" colIndex="8" cellId="9">This is a test...</TableCell>
            	</TableRow>
                <TableRow index="1">
                    <TableHandle rowIndex="1" />
            		<TableCell rowIndex="1" colIndex="0" cellId="11">This is a test...</TableCell>
                    <TableCell rowIndex="1" colIndex="1" cellId="12">This is a test...</TableCell>
                    <TableCell rowIndex="1" colIndex="2" cellId="13">This is a test...</TableCell>
                    <TableCell rowIndex="1" colIndex="3" cellId="14">This is a test...</TableCell>
                    <TableCell rowIndex="1" colIndex="4" cellId="15">This is a test...</TableCell>
                    <TableCell rowIndex="1" colIndex="5" cellId="16">This is a test...</TableCell>
                    <TableCell rowIndex="1" colIndex="6" cellId="17">This is a test...</TableCell>
                    <TableCell rowIndex="1" colIndex="7" cellId="18">This is a test...</TableCell>
                    <TableCell rowIndex="1" colIndex="8" cellId="19">This is a test...</TableCell>
                </TableRow>
                <TableRow index="2">
                    <TableHandle rowIndex="2" />
            		<TableCell rowIndex="2" colIndex="0" cellId="21">This is a test...</TableCell>
                    <TableCell rowIndex="2" colIndex="1" cellId="22">This is a test...</TableCell>
                    <TableCell rowIndex="2" colIndex="2" cellId="23">This is a test...</TableCell>
                    <TableCell rowIndex="2" colIndex="3" cellId="24">This is a test...</TableCell>
                    <TableCell rowIndex="2" colIndex="4" cellId="25">This is a test...</TableCell>
                    <TableCell rowIndex="2" colIndex="5" cellId="26">This is a test...</TableCell>
                    <TableCell rowIndex="2" colIndex="6" cellId="27">This is a test...</TableCell>
                    <TableCell rowIndex="2" colIndex="7" cellId="28">This is a test...</TableCell>
                    <TableCell rowIndex="2" colIndex="8" cellId="29">This is a test...</TableCell>
                </TableRow>
                <TableRow index="3">
                    <TableHandle rowIndex="3" />
            		<TableCell rowIndex="3" colIndex="0" cellId="31">This is a test...</TableCell>
                    <TableCell rowIndex="3" colIndex="1" cellId="32">This is a test...</TableCell>
                    <TableCell rowIndex="3" colIndex="2" cellId="33">This is a test...</TableCell>
                    <TableCell rowIndex="3" colIndex="3" cellId="34">This is a test...</TableCell>
                    <TableCell rowIndex="3" colIndex="4" cellId="35">This is a test...</TableCell>
                    <TableCell rowIndex="3" colIndex="5" cellId="36">This is a test...</TableCell>
                    <TableCell rowIndex="3" colIndex="6" cellId="37">This is a test...</TableCell>
                    <TableCell rowIndex="3" colIndex="7" cellId="38">This is a test...</TableCell>
                    <TableCell rowIndex="3" colIndex="8" cellId="39">This is a test...</TableCell>
                </TableRow>
                <TableRow index="4">
                    <TableHandle rowIndex="4" />
            		<TableCell rowIndex="4" colIndex="0" cellId="41">This is a test...</TableCell>
                    <TableCell rowIndex="4" colIndex="1" cellId="42">This is a test...</TableCell>
                    <TableCell rowIndex="4" colIndex="2" cellId="43">This is a test...</TableCell>
                    <TableCell rowIndex="4" colIndex="3" cellId="44">This is a test...</TableCell>
                    <TableCell rowIndex="4" colIndex="4" cellId="45">This is a test...</TableCell>
                    <TableCell rowIndex="4" colIndex="5" cellId="46">This is a test...</TableCell>
                    <TableCell rowIndex="4" colIndex="6" cellId="47">This is a test...</TableCell>
                    <TableCell rowIndex="4" colIndex="7" cellId="48">This is a test...</TableCell>
                    <TableCell rowIndex="4" colIndex="8" cellId="49">This is a test...</TableCell>
                </TableRow>
                <TableRow index="5">
                    <TableHandle rowIndex="5" />
            		<TableCell rowIndex="5" colIndex="0" cellId="51">This is a test...</TableCell>
                    <TableCell rowIndex="5" colIndex="1" cellId="52">This is a test...</TableCell>
                    <TableCell rowIndex="5" colIndex="2" cellId="53">This is a test...</TableCell>
                    <TableCell rowIndex="5" colIndex="3" cellId="54">This is a test...</TableCell>
                    <TableCell rowIndex="5" colIndex="4" cellId="55">This is a test...</TableCell>
                    <TableCell rowIndex="5" colIndex="5" cellId="56">This is a test...</TableCell>
                    <TableCell rowIndex="5" colIndex="6" cellId="57">This is a test...</TableCell>
                    <TableCell rowIndex="5" colIndex="7" cellId="58">This is a test...</TableCell>
                    <TableCell rowIndex="5" colIndex="8" cellId="59">This is a test...</TableCell>
                </TableRow>
            </tbody>
        </table>
    );
}

export default Table;
