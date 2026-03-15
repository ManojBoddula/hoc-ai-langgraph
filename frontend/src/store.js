// src/store.js
import { createStore } from "redux";

const initialState = { form: {}, messages: [] };

function reducer(state = initialState, action) {
  switch (action.type) {
    case "UPDATE_FORM":
      return { ...state, form: { ...state.form, ...action.payload } };
    case "ADD_MESSAGE":
      return { ...state, messages: [...state.messages, action.payload] };
    default:
      return state;
  }
}

export const store = createStore(reducer);