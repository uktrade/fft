
export const SET_SELECTED_ROW = 'SET_SELECTED_ROW';
export const ADD_SELECTED_CELL = 'ADD_SELECTED_CELL';
export const UNSELECT_ALL_CELLS = 'UNSELECT_ALL_CELLS';
export const SET_INITIAL_CELL = 'SET_INITIAL_CELL';
export const SET_LAST_CELL = 'SET_LAST_CELL';
export const IS_SELECTING = 'IS_SELECTING';

const selectionInitial = {
    row: null,
    cells: [],
    initialCell: null,
    lastCell: null,
    isSelecting: false
};

export const selection = (state = selectionInitial, action) => {
    switch (action.type) {
        case IS_SELECTING:
            return Object.assign({}, state, {
                isSelecting: action.isSelecting,
            });
        case SET_INITIAL_CELL:
            return Object.assign({}, state, {
                initialCell: action.cell,
            });
        case SET_LAST_CELL:
            return Object.assign({}, state, {
                lastCell: action.cell,
            });
        case SET_SELECTED_ROW:
            return Object.assign({}, state, {
                row: action.row,
                cells: []
            });
        case UNSELECT_ALL_CELLS:
            return Object.assign({}, state, {
                row: null,
                cells: []
            });
        case ADD_SELECTED_CELL:
            let idAlreadyExists = state.cells.indexOf(action.cell) > -1;
            // make a copy of the existing array
            let cells = state.cells.slice();

            if(idAlreadyExists) {
                //cells = cells.filter(id => id != action.cell);                
            }     
            else {
                // modify the COPY, not the original
                cells.push(action.cell);            
            }      

            return {
                // "spread" the original state object
                ...state,
                // but replace the "cells" field
                cells
            };
        default:
            return state;
    }
}
