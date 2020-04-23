import { createSlice } from '@reduxjs/toolkit';
// Use of this lib guarentees no state mutatation

const filter = createSlice({
    name: "filter",
    slice: 'edit',
    initialState: {
        open: false
    },
    reducers: {
        OPEN_FILTER_IF_CLOSED: (state, action) => {
            if (state.open)
                return

            state.open = true
        },
        TOGGLE_FILTER: (state, action) => {
            if (state.open) {
                state.open = false
            } else {
                state.open = true
            }
        },
    }
});

export const {
    TOGGLE_FILTER,
    OPEN_FILTER_IF_CLOSED,
} = filter.actions;

export default filter.reducer;
