import { createSlice } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const cellCount = createSlice({
    slice: 'cellCount',
    initialState: {
        cellCount: 0
    },
    reducers: {
        SET_CELL_COUNT: (state, action) => {
            state.cellCount = action.payload.cellCount
        }
    }
});

export const {
    SET_CELL_COUNT,
} = cellCount.actions;

export default cellCount.reducer;
