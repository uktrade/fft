import React, {Fragment, useState, useEffect, useRef } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import { RowProvider } from  '../../Components/RowContext'
import { 
    SELECT_CELL,
    UNSELECT_CELL,
    UNSELECT_ALL
} from '../../Reducers/Cells'

function TableRow({children, index}) {
    const dispatch = useDispatch();
    const allCells = useSelector(state => state.allCells);

    const selectRow = (rowIndex) => {

        dispatch({
            type: UNSELECT_ALL
        });

        dispatch({
            type: UNSELECT_CELL
        });

        for (let cellId in allCells) {
            let cell = allCells[cellId];
            if (cell.rowIndex == rowIndex) {
                dispatch(
                    SELECT_CELL({
                        id: cell.id
                    })
                );
            }
       }
    }

    const selectColumn = (colKey) => {
        dispatch({
            type: UNSELECT_ALL
        });

        for (let cellId in allCells) {
            let cell = allCells[cellId];
            if (cell.key == colKey) {
                dispatch(
                    SELECT_CELL({
                        id: cell.id
                    })
                );
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
