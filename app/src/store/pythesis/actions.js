export const QUERY_ARGS       = 'QUERY_ARGS'
export const QUERY_CONFIG     = 'QUERY_CONFIG'
export const CONSOLE_TOGGLE   = 'CONSOLE_TOGGLE'
export const CONSOLE_OUT      = 'CONSOLE_OUTPUT'
export const BUILD            = 'BUILD'
export const SELECT_FILE      = 'SELECT_FILE'
export const TRANSLATE_PAGES  = 'TRANSLATE_PAGES'
export const SET_PAGE_NUMBER  = 'SET_PAGE_NUMBER'
export const SET_NUM_PAGES    = 'SET_NUM_PAGES'
export const TRANSLATE_ZOOM   = 'TRANSLATE_ZOOM'
export const RELOAD           = 'RELOAD'

export const consoleOut = (consoleOut) => {
  return {
    type: CONSOLE_OUT,
    payload: {
      consoleOut: consoleOut
    }
  }
}

export const consoleToggle = () => {
  return (dispatch, getState) => {
    const { pythesis } = getState()
    return dispatch({
      type: CONSOLE_TOGGLE,
      payload: {
        consoleOpen: !pythesis.consoleOpen // Inverse open
      }
    })
  }
}

export const queryConfig = () => {
  return (dispatch, getState) => {
    fetch(`${process.env.REACT_APP_SERVER}/config`)
    .then(result => result.json())
    .then(result => {
      return dispatch({
        type: QUERY_CONFIG,
        payload: {
          config: result
        }
      })
    })
  }
}

export const build = () => {
  return (dispatch, getState) => {
    return dispatch({
      type: BUILD
    })
  }
}

export const setPageNumber = (pageNumber) => {
  return (dispatch, getState) => {
    const { pythesis } = getState()
    if (pageNumber > 0 && pageNumber < pythesis.numPages) {
      return dispatch({
        type: SET_PAGE_NUMBER,
        payload: {
          pageNumber: pageNumber
        }
      })
    }
  }
}

export const translatePages = (offset) => {
  return (dispatch, getState) => {
    const { pythesis } = getState()
    let n = pythesis.pageNumber + offset

    if (n > 0) {
      if (n <= pythesis.numPages) {
        // Only dispatch if page number is still valid:
        return dispatch({
          type: TRANSLATE_PAGES,
          payload: {
            pageNumber: n
          }
        })
      }
    }
  }
}

export const setNumPages = (numPages) => {
  return (dispatch, getState) => {
    return dispatch({
      type: SET_NUM_PAGES,
      payload: {
        numPages: numPages
      }
    })
  }
}

export const translateZoom = (offset) => {
  return (dispatch, getState) => {
    const { pythesis } = getState()
    let n = pythesis.zoom + offset
    if (n >= 0.5) {
      if (n <= 5) {
        return dispatch({
          type: TRANSLATE_ZOOM,
          payload: {
            zoom: n
          }
        })
      }
    }
  }
}

export const reload = () => {
  return (dispatch, getState) => {
    return dispatch({
      type: RELOAD
    })
  }
}
