import React, {Fragment, useState, useEffect, useRef } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';

import TableRow from '../../Components/TableRow/index'
import TableCell from '../../Components/TableCell/index'
import TableHandle from '../../Components/TableHandle/index'
import { SET_MOUSE_DOWN } from '../../Reducers/Mouse'
import { UNSELECT_ALL_CELLS, IS_SELECTING } from '../../Reducers/Selection'
import { SELECT_CELL, UNSELECT_CELL } from '../../Reducers/Cells'

function Table() {
    const dispatch = useDispatch();

    const captureMouseDn = (e) => {
        dispatch({
            type: UNSELECT_ALL_CELLS
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

    const initialCell = useSelector(state => state.selection.initialCell);
    const lastCell = useSelector(state => state.selection.lastCell);
	const selectedCells = useSelector(state => state.selection.cells);
    const allCells = useSelector(state => state.allCells.allCells);
    const isSelecting = useSelector(state => state.selection.isSelecting);

    console.log("initialCell", initialCell);
    console.log("lastCell", lastCell);

    const LEFT_TO_RIGHT = 'LEFT_TO_RIGHT';
    const RIGHT_TO_LEFT = 'RIGHT_TO_LEFT';

    const TOP_TO_BOTTOM = 'TOP_TO_BOTTOM';
    const BOTTOM_TO_TOP = 'BOTTOM_TO_TOP';

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

            if (initial.y > last.y) {
                // top to bottom
                verticalDirection = BOTTOM_TO_TOP
            }

			for (let cellId in allCells) {
                let cell = allCells[cellId];
                let selectable = false;
				//let cell = allCells["id_" + selected];

				console.log("cell.id", cell.id);
				console.log("cell.y", cell.rect.y);
				console.log("initial.y", initial.rect.y);

                if (
                    horizontalDirection == LEFT_TO_RIGHT &&
                    verticalDirection == TOP_TO_BOTTOM
                ) {
                    if (
                        cell.rect.y >= initial.rect.y &&
                        cell.rect.y <= last.rect.y &&
                        cell.rect.x <= last.rect.x &&
                        cell.rect.x >= initial.rect.x
                    ) {
                        selectable = true;
                    }
                } else {
                    if (
                        cell.rect.y <= initial.rect.y &&
                        cell.rect.y >= last.rect.y &&
                        cell.rect.x >= last.rect.x &&
                        cell.rect.x <= initial.rect.x
                    ) {
                        selectable = true;
                    }
                }

                if (selectable) {
                   dispatch({
                        type: SELECT_CELL,
                        id: cell.id
                    });
                } else {
                   dispatch({
                        type: UNSELECT_CELL,
                        id: cell.id
                    });
                }

                console.log("=====\\======");
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
        <table border="1">
            <tbody>
            	<TableRow index="0">
                    <TableHandle />
            		<TableCell cellId="1">This is a test...</TableCell>
                    <TableCell cellId="2">This is a test...</TableCell>
                    <TableCell cellId="3">This is a test...</TableCell>
                    <TableCell cellId="4">This is a test...</TableCell>
                    <TableCell cellId="5">This is a test...</TableCell>
                    <TableCell cellId="6">This is a test...</TableCell>
                    <TableCell cellId="7">This is a test...</TableCell>
                    <TableCell cellId="8">This is a test...</TableCell>
                    <TableCell cellId="9">This is a test...</TableCell>
            	</TableRow>
                <TableRow index="1">
                    <TableHandle />
            		<TableCell cellId="11">This is a test...</TableCell>
                    <TableCell cellId="12">This is a test...</TableCell>
                    <TableCell cellId="13">This is a test...</TableCell>
                    <TableCell cellId="14">This is a test...</TableCell>
                    <TableCell cellId="15">This is a test...</TableCell>
                    <TableCell cellId="16">This is a test...</TableCell>
                    <TableCell cellId="17">This is a test...</TableCell>
                    <TableCell cellId="18">This is a test...</TableCell>
                    <TableCell cellId="19">This is a test...</TableCell>
                </TableRow>
                <TableRow index="2">
                    <TableHandle />
            		<TableCell cellId="21">This is a test...</TableCell>
                    <TableCell cellId="22">This is a test...</TableCell>
                    <TableCell cellId="23">This is a test...</TableCell>
                    <TableCell cellId="24">This is a test...</TableCell>
                    <TableCell cellId="25">This is a test...</TableCell>
                    <TableCell cellId="26">This is a test...</TableCell>
                    <TableCell cellId="27">This is a test...</TableCell>
                    <TableCell cellId="28">This is a test...</TableCell>
                    <TableCell cellId="29">This is a test...</TableCell>
                </TableRow>
                <TableRow index="3">
                    <TableHandle />
            		<TableCell cellId="31">This is a test...</TableCell>
                    <TableCell cellId="32">This is a test...</TableCell>
                    <TableCell cellId="33">This is a test...</TableCell>
                    <TableCell cellId="34">This is a test...</TableCell>
                    <TableCell cellId="35">This is a test...</TableCell>
                    <TableCell cellId="36">This is a test...</TableCell>
                    <TableCell cellId="37">This is a test...</TableCell>
                    <TableCell cellId="38">This is a test...</TableCell>
                    <TableCell cellId="39">This is a test...</TableCell>
                </TableRow>
                <TableRow index="4">
                    <TableHandle />
            		<TableCell cellId="41">This is a test...</TableCell>
                    <TableCell cellId="42">This is a test...</TableCell>
                    <TableCell cellId="43">This is a test...</TableCell>
                    <TableCell cellId="44">This is a test...</TableCell>
                    <TableCell cellId="45">This is a test...</TableCell>
                    <TableCell cellId="46">This is a test...</TableCell>
                    <TableCell cellId="47">This is a test...</TableCell>
                    <TableCell cellId="48">This is a test...</TableCell>
                    <TableCell cellId="49">This is a test...</TableCell>
                </TableRow>
                <TableRow index="5">
                    <TableHandle />
            		<TableCell cellId="51">This is a test...</TableCell>
                    <TableCell cellId="52">This is a test...</TableCell>
                    <TableCell cellId="53">This is a test...</TableCell>
                    <TableCell cellId="54">This is a test...</TableCell>
                    <TableCell cellId="55">This is a test...</TableCell>
                    <TableCell cellId="56">This is a test...</TableCell>
                    <TableCell cellId="57">This is a test...</TableCell>
                    <TableCell cellId="58">This is a test...</TableCell>
                    <TableCell cellId="59">This is a test...</TableCell>
                </TableRow>
            </tbody>
        </table>
    );
}

export default Table;
