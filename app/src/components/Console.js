import './Console.css'
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import React, { Component } from 'react'

class Console extends Component {
  constructor(props) {
    super(props)
    this.consoleRef = React.createRef()
  }

  componentDidUpdate() {
    this.consoleRef.current.scrollIntoView(false)
  }

  render() {
    return(
      <div className="Console">
        <div className="output" ref={this.consoleRef}>
          {this.props.out}
        </div>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    consoleOut: state.pythesis.consoleOut
  }
}

export default connect(mapStateToProps)(Console)
