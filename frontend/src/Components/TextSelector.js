import React from 'react'
import './components.css'

const TextSelector = (props) => {
    return props.comments.map((item, index) => (
        <span key={item.id} id={item.id} className={
            `common-text ${item.highlightType === 'toxic' ? 'toxic-highlighted-text':
            item.highlightType === 'nontoxic'? 'nontoxic-highlighted-text' : 'unhighlighted-text'}`}>&nbsp;{item.text}&nbsp;</span>
    ))
}

export default TextSelector;
