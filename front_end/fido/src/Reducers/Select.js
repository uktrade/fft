import { createSlice, PayloadAction } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const select = createSlice({
    slice: 'select',
    initialState: {
        initial: null,
        last: null
    },
    reducers: {
        SET_INITIAL_CELL: (state, action) => {
            state["initial"] = action.payload.id
        },
        SET_LAST_CELL: (state, action) => {
            state["last"] = action.payload.id
        },
    }
});

export const {
    SET_INITIAL_CELL,
    SET_LAST_CELL,
} = select.actions;

export default select.reducer;
