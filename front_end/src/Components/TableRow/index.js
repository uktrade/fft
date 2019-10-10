import React, {Fragment, useState, useEffect, useRef } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import { RowProvider } from  '../../Components/RowContext'
import { 
    SELECT_CELL,
    UNSELECT_CELL,
    UNSELECT_ALL
} from '../../Reducers/Cells'
import {
    SET_INITIAL,
    SET_LAST
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
                        SET_INITIAL({
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

                // TODO - set this as actual last cell in row (needs to use array rather than object state)

                dispatch(
                    SET_LAST({
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
                        SET_INITIAL({
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
                    SET_LAST({
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
            <tr className="govuk-table__row">
                {children}
            </tr>
        </RowProvider>
    );
}

export default TableRow;
