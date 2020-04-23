import { createSlice } from '@reduxjs/toolkit';
// Use of this lib guarentees no state mutatation

const error = createSlice({
    name: "error",
    slice: 'error',
    initialState: {
        errorMessage: null
    },
    reducers: {
        SET_ERROR: (state, action) => {
            state.errorMessage = action.payload.errorMessage
        },
    }
});

export const {
    SET_ERROR,
} = error.actions;

export default error.reducer;
