import React, {Fragment, useState, useEffect, useRef } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import { RowProvider } from  '../../Components/RowContext'
import { 
    SELECT_CELL,
    UNSELECT_CELL,
    UNSELECT_ALL
} from '../../Reducers/Cells'
import {
    SET_INITIAL_CELL,
    SET_LAST_CELL
} from '../../Reducers/Select'

function TableRow({children, index}) {
    const dispatch = useDispatch();
    const allCells = useSelector(state => state.allCells);

    const selectRow = (rowIndex) => {

        dispatch(
            UNSELECT_ALL()
        );

        let setInital = false;

        for (let cellId in allCells) {
            let cell = allCells[cellId];
            if (cell.editable && cell.rowIndex == rowIndex) {
                if (!setInital) {
                    dispatch(
                        SET_INITIAL_CELL({
                            id: cellId
                        })
                    );
                    setInital = true;
                }

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
    }

    const selectColumn = (colKey) => {
        dispatch(
            UNSELECT_ALL()
        );
        let setInital = false;

        for (let cellId in allCells) {
            let cell = allCells[cellId];
            if (cell.key == colKey) {
                if (!setInital) {
                    dispatch(
                        SET_INITIAL_CELL({
                            id: cellId
                        })
                    );
                    setInital = true;
                }

                dispatch(
                    SELECT_CELL({
                        id: cell.id
                    })
                );

                dispatch(
                    SET_LAST_CELL({
                        id: cellId
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
