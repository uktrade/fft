import React, {Fragment, useState, useEffect, useRef } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import { RowProvider } from  '../../Components/RowContext'
import { SET_SELECTED_ROW } from '../../Reducers/Selection'
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

function TableRow({children, index}) {
    const dispatch = useDispatch();
    const allCells = useSelector(state => state.allCells);

    const selectRow = (rowIndex) => {

        dispatch({
            type: UNSELECT_ALL
        });

        dispatch({
            type: UNHIGHLIGHT_ALL
        });

        console.log(allCells);

        for (let cellId in allCells) {
            let cell = allCells[cellId];
            if (cell.rowIndex == rowIndex) {
                dispatch(
                    HIGHLIGHT_CELL({
                        id: cell.id
                    })
                );

                dispatch({
                    type: ADD_CELL_TO_SELECTION,
                    id: cell.id
                });
            }
       }
    }

    const selectColumn = (colIndex) => {
        dispatch({
            type: UNSELECT_ALL
        });

        dispatch({
            type: UNHIGHLIGHT_ALL
        });

        for (let cellId in allCells) {
            let cell = allCells[cellId];
            if (cell.colIndex == colIndex) {
                dispatch(
                    HIGHLIGHT_CELL({
                        id: cell.id
                    })
                );

                dispatch({
                    type: ADD_CELL_TO_SELECTION,
                    id: cell.id
                });
            }
       }
    }

    return (
        <RowProvider value={{ 
            selectRow: selectRow,
            selectColumn: selectColumn
        }}>
            <tr>
                {children}
            </tr>
        </RowProvider>
    );
}

export default TableRow;
