
export const SET_EDIT_CELL = 'SET_EDIT_CELL';

const editCellInitial = {
	cellId: null
}

export const editCell = (state = editCellInitial, action) => {
    switch (action.type) {
        case SET_EDIT_CELL:
            return Object.assign({}, state, {
            	cellId: action.cellId
            });
        default:
            return state;
    }
}
