
export const ADD_CELL = 'ADD_CELL';
export const SELECT_CELL = 'SELECT_CELL';
export const UNSELECT_CELL = 'UNSELECT_CELL';

const allCellsInitial = {
    allCells: {}
};

export const allCells = (state = allCellsInitial, action) => {
    switch (action.type) {
        case SELECT_CELL:
            var newState = state.allCells[action.id] = {
                id: state.allCells[action.id].id,
                rect: state.allCells[action.id].rect,
                selected: true
            }
            return Object.assign({}, state, {
                newState,
            });
        case UNSELECT_CELL:
            var newState = state.allCells[action.id] = {
                id: state.allCells[action.id].id,
                rect: state.allCells[action.id].rect,
                selected: false
            }
            return Object.assign({}, state, {
                newState,
            });
        case ADD_CELL:
            var newState = state.allCells[action.id] = {
                id: action.id,
                rect: action.rect,
                selected: false
            }
            return Object.assign({}, state, {
                newState,
            });
        default:
            return state;
    }
}
