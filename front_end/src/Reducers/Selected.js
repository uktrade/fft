import { createSlice } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const selected = createSlice({
    slice: 'select',
    initialState: {
        selectedRow: -1,
        all: false
    },
    reducers: {
        SET_SELECTED_ROW: (state, action) => {
            state.all = false
            state.selectedRow = action.payload.selectedRow
        },
        SELECT_ALL: (state, action) => {
            state.all = true
        },
        UNSELECT_ALL: (state, action) => {
            state.selectedRow = -1
            state.all = false
        },
    }
});

export const {
    SET_SELECTED_ROW,
    SELECT_ALL,
    UNSELECT_ALL
} = selected.actions;

export default selected.reducer;
