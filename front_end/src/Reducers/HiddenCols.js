import { createSlice } from "@reduxjs/toolkit";
// Use of this lib guarantees no state mutation

const defaultState = {
  hiddenCols: [],
  showAll: true,
};

const loadState = () => {
  const serializedState = localStorage.getItem("editForecast.hiddenCols");
  return serializedState ? JSON.parse(serializedState) : defaultState;
};

const saveState = (state) => {
  const serializedState = JSON.stringify(state);
  localStorage.setItem("editForecast.hiddenCols", serializedState);
};

const hiddenCols = createSlice({
  name: "hiddenCols",
  slice: "hidden",
  initialState: loadState(),
  reducers: {
    TOGGLE_ITEM: (state, action) => {
      let index = state.hiddenCols.indexOf(action.payload);
      if (index > -1) {
        state.hiddenCols.splice(index, 1);
      } else {
        state.showAll = false;
        state.hiddenCols.push(action.payload);
      }
      saveState(state);
    },
    TOGGLE_SHOW_ALL: (state, action) => {
      if (state.showAll) {
        state.showAll = false;
        state.hiddenCols = [
          "nac_code",
          "nac_description",
          "programme_code",
          "programme_description",
          "analysis1_code",
          "analysis2_code",
          "project_code",
        ];
      } else {
        state.showAll = true;
        // Turn on all cols
        state.hiddenCols = [];
      }
      saveState(state);
    },
  },
});

export const { TOGGLE_ITEM, TOGGLE_SHOW_ALL } = hiddenCols.actions;

export default hiddenCols.reducer;
