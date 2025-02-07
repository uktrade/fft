import { createSlice } from "@reduxjs/toolkit";

const allCells = createSlice({
  name: "allCells",
  slice: "allCells",
  initialState: {
    cells: [],
  },
  reducers: {
    SET_CELLS: (state, action) => {
      state.cells = action.payload.cells;
    },
  },
});

export const { SET_CELLS } = allCells.actions;

export default allCells.reducer;
