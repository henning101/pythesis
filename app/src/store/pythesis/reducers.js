import {
  QUERY_CONFIG, 
  QUERY_ARGS,
  CONSOLE_OUT,
  CONSOLE_TOGGLE,
  BUILD,
  TRANSLATE_PAGES,
  SET_PAGE_NUMBER,
  SET_NUM_PAGES,
  TRANSLATE_ZOOM,
  RELOAD
} from './actions'

const initialState = {
  consoleOut: 'PyThesis v1.0',
  numPages: 1,
  config: null,
  args: null,
  pageNumber: 1,
  timestamp: Date.now(),
  zoom: 1,
  uri: '',
  selectedProject: 0,
  consoleOpen: false,
  pdfPath: 'build/document.pdf'
}

export const pythesisReducer = (state = initialState, action) => {
  switch (action.type) {
    case CONSOLE_OUT: {
      return {
        ...state,
        consoleOut: action.payload.consoleOut
      }
    }
    case CONSOLE_TOGGLE: {
      return {
        ...state,
        consoleOpen: action.payload.consoleOpen
      }
    }
    case QUERY_CONFIG: {
      return {
        ...state,
        config: action.payload.config
      }
    }
    case QUERY_ARGS: {
      return {
        ...state,
        args: action.payload.args
      }
    }
    case BUILD: {
      return {
        ...state,
        uri: action.payload.uri
      }
    }
    case TRANSLATE_PAGES: {
      return {
        ...state,
        pageNumber: action.payload.pageNumber
      }
    }
    case SET_PAGE_NUMBER: {
      return {
        ...state,
        pageNumber: action.payload.pageNumber
      }
    }
    case SET_NUM_PAGES: {
      return {
        ...state,
        numPages: action.payload.numPages
      }
    }
    case TRANSLATE_ZOOM: {
      return {
        ...state,
        zoom: action.payload.zoom
      }
    }
    case RELOAD: {
      return {
        ...state,
        uri: action.payload.uri
      }
    }
    default: {
      return state
    }
  }
}
