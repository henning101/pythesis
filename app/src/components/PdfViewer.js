import React from 'react'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'
import {
  consoleOut,
  consoleToggle,
  translatePages,
  setPageNumber, 
  translateZoom,
  setNumPages
} from '../store/pythesis/actions'
import { Document, PDFViewer, Page, pdfjs } from 'react-pdf'
import loadingSvg from './loading.svg'
import './PdfViewer.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {
  faArrowLeft,
  faArrowRight,
  faTerminal,
  faPlay,
  faSync,
  faSearchPlus,
  faSearchMinus
} from '@fortawesome/free-solid-svg-icons'
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`

class PdfViewer extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      timestamp: Date.now(),
      buildResult: '',
      loading: false,
      output: 'PyThesis - A LaTeX Transpiler'
    }

    this.zoomIncrement = 0.02
    this.viewerRef = React.createRef()
    this.documentRef = React.createRef()
    this.pageNumberRef = React.createRef()
  }
  onDocumentLoadSuccess = ({ numPages }) => {
    this.props.dispatch(setNumPages(numPages))
  }

  componentDidMount() {
    this.viewerRef.current.focus()
  }

  render() {
    return (
      <div className="PdfViewer"
        ref={this.viewerRef}
        tabIndex="1"
        onKeyDown={
          (e) => {
            this.handleKeyDown(e)
          }
        }>
        <div className="document-container">
          {this.document()}
        </div>
        <div className="controls">
          <button
            onClick={(e) => {this.props.dispatch(translatePages(-1))}}>
            <FontAwesomeIcon icon={faArrowLeft} />
          </button>
          <button
            onClick={(e) => {this.props.dispatch(translatePages(1))}}>
            <FontAwesomeIcon icon={faArrowRight} />
          </button>
          <button
            onClick={(e) => {this.fullBuild()}}>
            <FontAwesomeIcon icon={faPlay} />
          </button>
          <button
            onClick={(e) => {this.setState({timestamp: Date.now()})}}>
            <FontAwesomeIcon icon={faSync} />
          </button>
          <button onClick={(e) => {this.props.dispatch(translateZoom(this.zoomIncrement))}}>
            <FontAwesomeIcon icon={faSearchPlus} />
          </button>
          <button onClick={(e) => {this.props.dispatch(translateZoom(-this.zoomIncrement))}}>
            <FontAwesomeIcon icon={faSearchMinus} />
          </button>
          <button onClick={(e) => {this.props.dispatch(consoleToggle())}}>
            <FontAwesomeIcon icon={faTerminal} />
          </button>
        </div>
        <div className="jump-to">
          <span className="label">Jump to page:</span>
          <input
            type="text"
            ref={this.pageNumberRef}
            onClick={e => {
              this.pageNumberRef.current.value = ''
            }}
            onKeyPress={e => {
              e.stopPropagation()
              if (e.charCode == 13) { // Enter
                const pageNumber = parseInt(this.pageNumberRef.current.value)
                this.props.dispatch(setPageNumber(pageNumber))
                this.pageNumberRef.current.value = ''
              }
            }}
          />
        </div>
        <div className="page">
          Page {this.props.pythesis.pageNumber} of {this.props.pythesis.numPages}
        </div>
        <img
            className="loading" 
            src={loadingSvg} 
            style={this.state.loading ? {display: 'block'} : {display: 'none'}}/>
      </div>
    );
  }

  document() {
    let width = 600
    if (this.viewerRef.current) {
      width = this.viewerRef.current.clientWidth * 0.4
    }
    width = width * this.props.pythesis.zoom

    const projectIndex = this.props.pythesis.selectedProject
    let uri = `${process.env.REACT_APP_SERVER}/pdf?timestamp=${this.state.timestamp}`

    return(
      <div
        className="document"
        style={{width: width}}
        ref={this.documentRef}>
        <Document
          file={uri}
          onLoadSuccess={this.onDocumentLoadSuccess}>
          <Page
            pageNumber={this.props.pythesis.pageNumber}
            size="A4"
            wrap={false}
            width={width} />
        </Document>
      </div>
    )
  }

  fullBuild() {
    this.build(`${process.env.REACT_APP_SERVER}/full_build`)
  }

  partialBuild() {
    this.build(`${process.env.REACT_APP_SERVER}/partial_build`)
  }

  partialExecute() {
    this.build(`${process.env.REACT_APP_SERVER}/partial_execute`)
  }

  build(buildUrl) {
    this.setState({
      loading: true,
      output: 'Building document ...'
    })

    fetch(buildUrl)
    .then((response) => {
      response.text()
      .then((text) => {
        this.setState({
          timestamp: Date.now(), // Trigger document reload,
          loading: false
        })
        this.props.dispatch(consoleOut(text))
      })
    })
    .catch((err) => {
      this.setState({
        output: err,
        loading: false
      })
    })
  }

  handleKeyDown(e) {
    switch (e.keyCode) {
      case 39: { // Arrow right
        this.props.dispatch(translatePages(1))
        break
      }
      case 37: { // Arrow left
        this.props.dispatch(translatePages(-1))
        break
      }
      case 107: { // Add
        this.props.dispatch(translateZoom(this.zoomIncrement))
        break
      }
      case 109: { // Subtract
        this.props.dispatch(translateZoom(-this.zoomIncrement))
        break
      }
      case 82: { // r
        this.setState({
          timestamp: Date.now() // Force reload
        })
        break
      }
      case 66: { // b
        this.fullBuild()
        break
      }
      case 80: { // p
        this.partialBuild()
        break
      }
      case 69: { // e
        this.partialExecute()
        break
      }
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
      consoleToggle,
      translatePages,
      translateZoom,
      setNumPages
    }),
    dispatch
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(PdfViewer)
