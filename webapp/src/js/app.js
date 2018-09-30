const React = require('react');
const ReactDOM = require('react-dom')

class App extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			book: {
				title: undefined,
				author: undefined,
				asin: undefined
			},
			highlights: []
		};
	}

	getInitialState() {
		console.log('--- initial state');
	}

	componentWillMount() {
		console.log('----- componentWillMount');
	}

	render() {
		console.log('----- render');
		const list = this.state.highlights
			//.filter((target) => {
			//	return target.startsWith("A");
			//})
			.map((target) => {
				console.log(target);
				return <li key={target.location}>{target.text}</li>
			});
		return (
			<div>
			<ul>{list}</ul>
			</div>
		);
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

}

ReactDOM.render(
	<App />,
	document.getElementById('app')
)

alert('aaaaz');
