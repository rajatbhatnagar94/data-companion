import React from 'react'
import { Card, Image } from 'semantic-ui-react'
import './components.css'
import TextSelector from './TextSelector'

const onLinkClick = (commentUrl) => {
    window.open(commentUrl, "_blank");
}

const RedditCard = (props) => {
  const { predicted_label } = props
  const cardStyles = {minWidth: '300px'}
  let toxicity_text = 'You are not the asshole';
  let color = 'green';
  if (predicted_label === 1) {
    toxicity_text = 'You are the asshole';
    color = 'red';
  } else if (predicted_label === 2) {
    toxicity_text = 'Everyone sucks here';
    color = 'red';
  } else if (predicted_label === 3) {
    toxicity_text = 'No assholes here';
    color = 'red';
  }

  return (
    <Card style={cardStyles}>
      <Card.Content>
        <Image
          floated='right'
          size='mini'
          src={props.author_icon_img}
        />
        <Card.Header>{props.author_name}</Card.Header>
        <Card.Meta>{props.created_at}</Card.Meta>
        <Card.Description className={'reddit-card-description'}>
          <TextSelector comments={props.rationale}></TextSelector>
          <span title="Go to Reddit comment" className="reddit-comment-link" onClick={onLinkClick.bind(null, props.comment_url)}>&#x1F517;</span>
        </Card.Description>
      </Card.Content>
      <Card.Content extra>
        <div style={{color: color}}>
          {toxicity_text}
        </div>
      </Card.Content>
    </Card>
  );
}

export default RedditCard
