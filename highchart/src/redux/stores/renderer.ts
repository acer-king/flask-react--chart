import { combineReducers } from "redux";
import { configureStore } from "@reduxjs/toolkit";
import commonSlice from "../slices/commonSlice";

const rootReducer = combineReducers({
  commonProps: commonSlice.reducer,
});

const store = configureStore({
  reducer: rootReducer,
});

export default store;
export type AppState = ReturnType<typeof rootReducer>;
