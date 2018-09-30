const React = require('react');
const ReactDOM = require('react-dom')

class App extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			book: undefined,
			highlights: undefined
		};
	}

	getInitialState() {
		console.log('--- initial state');
	}

	componentDidMount() {
		console.log('----- componentDidMount');
		$.ajax({
			url: '/api/json/book',
			type: 'GET',
			dataType: 'json',
			success: (res) => {
				console.log('----- res');
				console.log(res);
				this.setState({
					book: res.book,
					highlights: res.highlights
				});
			}.bind(this),
			error: (xhr, status, err) => {
				console.log(status, err.toString());
			}.bind(this)
		});
	}

	render() {
		console.log('this.state');
		console.log(this.state);
		const list = this.state.targets
			//.filter((target) => {
			//	return target.startsWith("A");
			//})
			.map((target) => {
				return <li key={target}>{target}</li>
			});
		return (
			<div>
			<ul>{list}</ul>
			</div>
		);
	}
}

ReactDOM.render(
	<App />,
	document.getElementById('app')
)

alert('aaaad');
