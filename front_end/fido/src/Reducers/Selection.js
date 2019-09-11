
export const SET_SELECTED_ROW = 'SET_SELECTED_ROW';
export const ADD_SELECTED_CELL = 'ADD_SELECTED_CELL';

const selectionInitial = {
    row: null,
    cells: []
};

function insertItem(array, action) {
  return [
    ...array.slice(0, action.index),
    action.cell,
    ...array.slice(action.index)
  ]
}

function updateObjectInArray(array, action) {
  return array.map((item, index) => {
    if (index !== action.index) {
      // This isn't the item we care about - keep it as-is
      return item
    }

    // Otherwise, this is the one we want - return an updated value
    return {
      ...item,
      ...action.cell
    }
  })
}

export const selection = (state = selectionInitial, action) => {
	console.log("state", state);
    switch (action.type) {
        case SET_SELECTED_ROW:
            return Object.assign({}, state, {
                row: action.row,
                cells: []
            });
        case ADD_SELECTED_CELL:
            let idAlreadyExists = state.cells.indexOf(action.cell) > -1;
            // make a copy of the existing array
            let cells = state.cells.slice();

            if(idAlreadyExists) {
                cells = cells.filter(id => id != action.cell);                
            }     
            else {
                // modify the COPY, not the original
                cells.push(action.cell);            
            }      

            return {
                // "spread" the original state object
                ...state,
                // but replace the "cells" field
                cells
            };
        default:
            return state;
    }
}
