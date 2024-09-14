import { createSlice } from '@reduxjs/toolkit';
// Use of this lib guarentees no state mutatation

const selected = createSlice({
    name: "selected",
    slice: 'select',
    initialState: {
        selectedRow: -1,
        employeeSelectedRow: -1,
        nonEmployeeSelectedRow: -1,
        all: false
    },
    reducers: {
        SET_SELECTED_ROW: (state, action) => {
            state.all = false
            state.selectedRow = action.payload.selectedRow
        },
        SELECT_ALL: (state, action) => {
            state.all = true
            state.selectedRow = -1
            state.nonEmployeeSelectedRow = -1
            state.employeeSelectedRow = -1
        },
        UNSELECT_ALL: (state, action) => {
            state.all = false
            state.selectedRow = -1
            state.nonEmployeeSelectedRow = -1
            state.employeeSelectedRow = -1
        },
        SET_EMPLOYEE_SELECTED_ROW: (state, action) => {
            state.all = false
            state.nonEmployeeSelectedRow = -1
            state.employeeSelectedRow = action.payload.employeeSelectedRow
        },
        SET_NON_EMPLOYEE_SELECTED_ROW: (state, action) => {
            state.all = false
            state.nonEmployeeSelectedRow = action.payload.nonEmployeeSelectedRow
            state.employeeSelectedRow = -1
        }
    }
});

export const {
    SET_SELECTED_ROW,
    SELECT_ALL,
    UNSELECT_ALL,
    SET_EMPLOYEE_SELECTED_ROW,
    SET_NON_EMPLOYEE_SELECTED_ROW,
} = selected.actions;

export default selected.reducer;
