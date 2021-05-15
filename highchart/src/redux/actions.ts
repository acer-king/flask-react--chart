
import * as commonPropSlice from "./slices/commonSlice";


export const actions = {
  SET_LOADING_STATE: commonPropSlice.setIsLoading,
  SET_DATA:commonPropSlice.setData,
};

export type ActionKeys = keyof typeof actions;
