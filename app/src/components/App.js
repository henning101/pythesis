import React, { Component } from 'react'
import { Resize, ResizeVertical, ResizeHorizon } from "react-resize-layout";
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { queryConfig } from '../store/pythesis/actions'
import PdfViewer from './PdfViewer'
import Console from './Console'
import './App.css'

class App extends Component {
  constructor(props) {
    super(props)
  }

  componentDidMount() {
    this.props.dispatch(queryConfig())
  }

  render() {
    return (
      <div className="App">
        {this.components()}
      </div>
    )
  }

  components() {
    console.log('Props: ')
    console.log(this.props)
    if (this.props.consoleOpen) {
      return(
        <Resize handleWidth="5px" handleColor="#fff">
          <ResizeVertical height="80%" minHeight="20px">
            <PdfViewer />
          </ResizeVertical>
          <ResizeVertical height="160px" minHeight="20px">
            <Console/>
          </ResizeVertical>
        </Resize>
      )
    }
    else {
      return <PdfViewer />
    }
  }
}

const mapStateToProps = (state) => {
  return {
    consoleOpen: state.pythesis.consoleOpen
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    ...bindActionCreators({
      queryConfig
    }),
    dispatch
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App)
