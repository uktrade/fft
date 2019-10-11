import { createSlice, PayloadAction } from 'redux-starter-kit';
// Use of this lib guarentees no state mutatation

const edit = createSlice({
    slice: 'select',
    initialState: {
        rect:{
            x: 0,
            y: 0,
            width: 0,
            height: 0
        },
        content: ""
    },
    reducers: {
        SET_EDIT_CELL: (state, action) => {
            //console.log(action.payload.rect)
            state.rect = action.payload.rect
            state.content = action.payload.content
        },
    }
});

export const {
    SET_EDIT_CELL,
} = edit.actions;

export default edit.reducer;
