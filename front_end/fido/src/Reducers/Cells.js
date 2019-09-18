import { createSlice, PayloadAction } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const allCells = createSlice({
    slice: 'allCells',
    initialState: {},
    reducers: {
        ADD_CELL: (state, action) => {
            state[action.payload.id] = {
                id: action.payload.id,
                key: action.payload.key,
                value: action.payload.value,
                rowIndex: action.payload.rowIndex,
                // rect: action.payload.rect,
                selected: false,
                edited: false
            }
        },
        SET_RECT: (state, action) => {
            state[action.payload.id]["rect"] = action.payload.rect;
        },
        SELECT_CELL: (state, action) => {
            //alert('Hier...');
            state[action.payload.id]["selected"] = true;
        },
        UNSELECT_CELL: (state, action) => {
            state[action.payload.id]["selected"] = false;
        },
        SET_EDITED: (state, action) => {
            state[action.payload.id]["edited"] = true;
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
    SET_RECT
} = allCells.actions;

export default allCells.reducer;
