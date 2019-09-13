// import { createSlice, PayloadAction } from 'redux-starter-kit';
// // Use of this lib guarentees no state mutatation

// const editCell = createSlice({
//     slice: 'editCell',
//     initialState: 44,
//     reducers: {
//         SET_EDIT_CELL: (state, action) => {
//         	console.log("action", action.payload.cellId);
//             state = action.payload.cellId
//         }
//     }
// });

// export const { 
//     SET_EDIT_CELL 
// } = editCell.actions;

// export default editCell.reducer;

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
