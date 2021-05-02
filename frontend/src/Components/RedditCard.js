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
        {predicted_label}
      </Card.Content>
    </Card>
  );
}

export default RedditCard
