import { createSlice, PayloadAction } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const allCells = createSlice({
    slice: 'allCells',
    initialState: {},
    reducers: {
        ADD_CELL: (state, action) => {
            state[action.payload.id] = {
                id: action.payload.id,
                rect: action.payload.rect,
                highlight: false,
                //isEditing: false
            }
        },
        HIGHLIGHT_CELL: (state, action) => {
            state[action.payload.id]["highlight"] = true;
        },
        UNHIGHLIGHT_CELL: (state, action) => {
            state[action.payload.id]["highlight"] = false;
        },
        // SET_EDITING: (state, action) => {
        //     state[action.payload.id]["isEditing"] = true;
        // },
        UNHIGHLIGHT_ALL: (state, action) => {
            for (var cellId in state.allCells) {
                state[cellId]["highlight"] = false;
            }
        }
    }
});

export const { 
    ADD_CELL, 
    HIGHLIGHT_CELL, 
    UNHIGHLIGHT_CELL, 
    SET_EDITING, 
    UNHIGHLIGHT_ALL 
} = allCells.actions;

export default allCells.reducer;
