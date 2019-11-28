import { createStore, combineReducers } from 'redux';
// import { persistReducer } from 'redux-persist';
// import storage from 'redux-persist/lib/storage';

import allCells from './Reducers/Cells';
import selected from './Reducers/Selected';
import showHideCols from './Reducers/ShowHideCols';
import edit from './Reducers/Edit';
import error from './Reducers/Error';

// const persistConfig = {
//     key: 'root',
//     //transforms: [encryptor],
//     storage
// }

const appReducer = combineReducers({
	selected,
    allCells,
    showHideCols,
    edit,
    error,
});

// const persistedReducer = persistReducer(persistConfig, appReducer)

//export const store = createStore(persistedReducer);
export const store = createStore(appReducer);
//export const persistor = persistStore(store);
export const purge = () => {
    //persistor.purge();
    localStorage.clear();
};
