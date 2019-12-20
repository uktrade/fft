import { createSlice } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const showHideCols = createSlice({
    slice: 'showHideCols',
    initialState: {
        nac: true,
        programme: true,
        analysis1: true,
        analysis2: true,
        projectCode:true
    },
    reducers: {
        TOGGLE_NAC: (state, action) => {
            state.nac = !state.nac
        },
        TOGGLE_PROG: (state, action) => {
            state.programme = !state.programme
        },
        TOGGLE_AN1: (state, action) => {
            state.analysis1 = !state.analysis1
        },
        TOGGLE_AN2: (state, action) => {
            state.analysis2 = !state.analysis2
        },
        TOGGLE_PROJ_CODE: (state, action) => {
            state.projectCode = !state.projectCode
        }
    }
});

export const {
    TOGGLE_NAC,
    TOGGLE_PROG,
    TOGGLE_AN1,
    TOGGLE_AN2,
    TOGGLE_PROJ_CODE
} = showHideCols.actions;

export default showHideCols.reducer;
