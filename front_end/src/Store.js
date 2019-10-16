import { createStore, combineReducers } from 'redux';
// import { persistReducer } from 'redux-persist';
// import storage from 'redux-persist/lib/storage';
import { mouse } from './Reducers/Mouse';
import allCells from './Reducers/Cells';
import edit from './Reducers/Edit'
import select from './Reducers/Select'

// const persistConfig = {
//     key: 'root',
//     //transforms: [encryptor],
//     storage
// }

const appReducer = combineReducers({
    mouse,
    allCells,
    edit,
    select,
});

// const persistedReducer = persistReducer(persistConfig, appReducer)

//export const store = createStore(persistedReducer);
export const store = createStore(appReducer);
//export const persistor = persistStore(store);
export const purge = () => {
    //persistor.purge();
    localStorage.clear();
};
