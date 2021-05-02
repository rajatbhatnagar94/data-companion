import React from 'react'
import { Link } from 'react-router-dom';
import Instructions from './Instructions';

class Header extends React.Component {
	render() {
			return (
					<React.Fragment>
						<div className="App-header">
							{
								this.props.showBackButton ?
								<div title="Go back" className="back-div">
									<Link to="/" className="back-link">&#10229;</Link>
								</div>: null
							}
								<h5 className={'username'}>Welcome User!</h5>
							<div className='app-logo-container'>
								<Link to='/'>
									<img src={"/reddit-logo.png"} className="app-logo" alt="reddit-logo" />
								</Link>
							</div>

							<div className="reddit-header-text">
								Welcome to r/AmITheAsshole
							</div>
						</div>
						<Instructions />
						</React.Fragment>
			)
	}
}

export default Header
