
export const ADD_CELL = 'ADD_CELL';
export const SELECT_CELL = 'SELECT_CELL';
export const UNSELECT_CELL = 'UNSELECT_CELL';
export const SET_EDITING = 'SET_EDITING';

const allCellsInitial = {
    allCells: {}
};

export const allCells = (state = allCellsInitial, action) => {
    switch (action.type) {
        case ADD_CELL:
            var newState = state.allCells[action.id] = {
                id: action.id,
                rect: action.rect,
                selected: false,
                isEditing: false
            }
            return Object.assign({}, state, {
                newState,
            });
        case SELECT_CELL:
            newState = state.allCells[action.id]["selected"] = true
            return Object.assign({}, state, {
                newState,
            });
        case UNSELECT_CELL:
            newState = state.allCells[action.id]["selected"] = false
            return Object.assign({}, state, {
                newState,
            });
        case SET_EDITING:
            newState = state.allCells[action.id]["isEditing"] = false
            return Object.assign({}, state, {
                newState,
            });
        default:
            return state;
    }
}
