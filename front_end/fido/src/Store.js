'use strict';

import { createStore, combineReducers } from 'redux';
import { persistStore, persistReducer } from 'redux-persist';
import { selection } from './Reducers/Selection';
import storage from 'redux-persist/lib/storage';


const persistConfig = {
    key: 'root',
    //transforms: [encryptor],
    storage
}

const appReducer = combineReducers({
    selection,
});

const persistedReducer = persistReducer(persistConfig, appReducer)

export const store = createStore(persistedReducer);
export const persistor = persistStore(store);
export const purge = () => {
    persistor.purge();
    localStorage.clear();
};
