import React, { Component, Fragment } from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import { selectProject, consoleOut } from '../store/pythesis/actions'
import './FileBrowser.css'

class FileBrowser extends Component {
  constructor(props) {
    super(props)
  }

  render() {
    return(
      <div className="FileBrowser">
        <h2>Project</h2>
      </div>
    )
  }

  projects() {
    if (this.props.pythesis.config !== null) {
      return this.props.pythesis.config.projects.map((project, index) => {
        return(
          <div
            className={'project ' + ((this.props.projectId === project.id) ? 'selected': '')}
            onClick={(e) => {
              this.props.dispatch(
                consoleOut(`Project selected: ${JSON.stringify(project, null, 2)}`)
              )
              this.props.dispatch(
                selectProject(index)
              )
            }}>
            {project.name}
          </div>
        )
      })
    } else {
      return ''
    }
  }
}

const mapStateToProps = (state) => {
  return {
    ...state,
    pythesis: state.pythesis
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    ...bindActionCreators({
      consoleOut,
      selectProject,
    }),
    dispatch
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(FileBrowser)
