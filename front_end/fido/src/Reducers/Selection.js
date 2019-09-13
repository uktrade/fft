
export const SET_SELECTED_ROW = 'SET_SELECTED_ROW';
export const SET_INITIAL_CELL = 'SET_INITIAL_CELL';
export const SET_LAST_CELL = 'SET_LAST_CELL';
export const IS_SELECTING = 'IS_SELECTING';
export const UNSELECT_ALL = 'UNSELECT_ALL';
export const ADD_CELL_TO_SELECTION = 'ADD_CELL_TO_SELECTION';

const selectionInitial = {
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
        case UNSELECT_ALL:
            return Object.assign({}, state, {
                row: null,
                cells: []
            });
        case ADD_CELL_TO_SELECTION:
            let idPresent = state.cells.indexOf(action.cell) > -1;
            let cells = state.cells.slice();

            if(idPresent) {
                return state;               
            }     
            else {
                
                cells.push(action.cell);            
            }      

            return {
                ...state,
                cells
            };
        default:
            return state;
    }
}
