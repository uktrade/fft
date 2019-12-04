export const SET_CELLS = 'SET_CELLS';

const cellsInitial = {
    cells: []
};

export const allCells = (state = cellsInitial, action) => {
    switch (action.type) {
        case SET_CELLS:
            console.log(action)
            return Object.assign({}, state, {
                cells: action.cells
            });
        default:
            return state;
    }
}