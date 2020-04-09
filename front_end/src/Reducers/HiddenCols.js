import { createSlice } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const hiddenCols = createSlice({
    slice: 'hidden',
    initialState: {
        hiddenCols: [],
        showAll: true
    },
    reducers: {
        TOGGLE_ITEM: (state, action) => {
            let index = state.hiddenCols.indexOf(action.payload)
            if (index > -1) {
                state.hiddenCols.splice(index, 1)
            } else {
                state.showAll = false
                state.hiddenCols.push(action.payload)
            }
        },
        TOGGLE_SHOW_ALL: (state, action) => {
            if (state.showAll) {
                state.showAll = false
                state.hiddenCols = [
                    "natural_account_code",
                    "programme",
                    "analysis1_code",
                    "analysis2_code",
                    "project_code"
                ]
            } else {
                state.showAll = true
                // Turn on all cols
                state.hiddenCols = []
            }
        },
    }
});

export const {
    TOGGLE_ITEM,
    TOGGLE_SHOW_ALL
} = hiddenCols.actions;

export default hiddenCols.reducer;
