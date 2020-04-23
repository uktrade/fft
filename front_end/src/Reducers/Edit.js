import { createSlice } from '@reduxjs/toolkit';
// Use of this lib guarentees no state mutatation

const edit = createSlice({
    name: "edit",
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
