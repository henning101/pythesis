import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { composeWithDevTools } from 'redux-devtools-extension'
import { pythesisReducer } from './pythesis/reducers'
import { logger }  from 'redux-logger'

const rootReducer = combineReducers({
  pythesis: pythesisReducer
})

const store = createStore(
  rootReducer,
  composeWithDevTools(applyMiddleware(thunk, logger))
)

export default store
