import React from 'react';
import { Select, Button } from 'semantic-ui-react'

const Pagination = ({ value, options, onChange, onButtonClick }) => {
	return (
		<div>
			<span>Page Size:&ensp;</span>
			<Select
				className="selection-pagination"
				value={value}
				options={options}
				onChange={onChange}
				placeholder="Page Size"
			/>&ensp;
			<Button
				onClick={onButtonClick}
				secondary
				content={`Load ${value} More`}
			/>
		</div>
	)
};

export default Pagination;
