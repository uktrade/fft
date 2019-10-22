import { createSlice } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const allCells = createSlice({
    slice: 'allCells',
    initialState: {},
    reducers: {
        ADD_CELL: (state, action) => {
            state[action.payload.id] = {
                index: action.payload.index,
                programmeCode: action.payload.programmeCode,
                naturalAccountCode: action.payload.naturalAccountCode,
                projectCode: action.payload.projectCode,
                id: action.payload.id,
                key: action.payload.key,
                editable: action.payload.editable,
                value: action.payload.value,
                rowIndex: action.payload.rowIndex,
                rect: null,
                selected: false,
                edited: false
            }
        },
        SET_RECT: (state, action) => {
            state[action.payload.id]["rect"] = action.payload.rect;
        },
        SELECT_CELL: (state, action) => {
            state[action.payload.id]["selected"] = true;
        },
        UNSELECT_CELL: (state, action) => {
            state[action.payload.id]["selected"] = false;
        },
        SET_EDITED: (state, action) => {
            state[action.payload.id]["edited"] = true;
        },
        SET_VALUE: (state, action) => {
            state[action.payload.id]["value"] = action.payload.value;
        },
        UNSELECT_ALL: (state, action) => {
            for (var cellId in state) {
                state[cellId]["selected"] = false;
            }
        }
    }
});

export const { 
    ADD_CELL, 
    SELECT_CELL,
    UNSELECT_CELL,
    SET_EDITED,
    UNSELECT_ALL,
    SET_RECT,
    SET_VALUE
} = allCells.actions;

export default allCells.reducer;
