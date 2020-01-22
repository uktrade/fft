import { createSlice } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const hiddenCols = createSlice({
    slice: 'hidden',
    initialState: {
        hiddenCols: []
    },
    reducers: {
        TOGGLE_ITEM: (state, action) => {
            let index = state.hiddenCols.indexOf(action.payload)
            if (index > -1) {
               state.hiddenCols.splice(index, 1);
            } else {
                state.hiddenCols.push(action.payload)
            }
        },
    }
});

export const {
    TOGGLE_ITEM,
} = hiddenCols.actions;

export default hiddenCols.reducer;
