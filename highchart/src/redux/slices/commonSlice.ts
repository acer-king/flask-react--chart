/* eslint-disable no-param-reassign */
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

const initialState = {
  isLoading: false,
  data:[]
}

type commonPropState = typeof initialState;

const commonPropSlice = createSlice({
  name: "commonProp",
  initialState,
  reducers: {
    setIsLoading: (
      state: commonPropState,
      action: PayloadAction<boolean>
    ): void => {
      state.isLoading = action.payload;
    },
    setData: (
      state: commonPropState,
      action: PayloadAction<any>
    ): void => {
      state.data = action.payload
    }
  },
});

export const { setIsLoading,setData } = commonPropSlice.actions;

export default commonPropSlice;
