import { createSlice } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const edit = createSlice({
    slice: 'edit',
    initialState: {
        cellId: null
    },
    reducers: {
        SET_EDITING_CELL: (state, action) => {
            state.cellId = action.payload.cellId
        },
    }
});

export const {
    SET_EDITING_CELL,
} = edit.actions;

export default edit.reducer;
