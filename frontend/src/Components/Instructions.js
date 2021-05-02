import React from 'react';
import { List, Item, Accordion } from 'semantic-ui-react';

const panel = [
  {
    key: 'Instructions',
    title: 'Instructions',
		content: {
			content: (
				<List className="list-styles" bulleted>
					<Item>Please enter a text to find out whether you were an Asshole in the situation</Item>
					<Item>On the left hand side you could see the various classified posts of r/AmITheAsshole</Item>
					<Item>Disclaimer: This website is built for the class: CSCI 4802-5802 at the University of Colorado Boulder</Item>
				</List>
			),
		}
  },
];
const Instructions = () => {
	return (
		<Accordion fluid defaultActiveIndex={0} panels={panel} />
	)
}

export default Instructions;
