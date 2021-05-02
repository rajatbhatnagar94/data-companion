import React from 'react'
import axios from 'axios';
import {withRouter} from 'react-router-dom';
import config from '../config'
import { Card } from 'semantic-ui-react'
import RedditCard from "./RedditCard"
import CardLoader from "./CardLoader"
import { withCookies } from 'react-cookie';
import Pagination from './Pagination'

const TOXIC = 'toxic'  // To be matched with the db value. Change with caution
const NON_TOXIC = 'non_toxic'  // To be matched with the db value. Change with caution
const PROBABLY_TOXIC = 'probably_toxic'
const AGREE = 'agree'
const DISAGREE = 'disagree'
const DONE = 'done'

const options = [{ text: 'Select Page Size', key: '', value: '', disabled: true }].concat([10, 15, 20, 50, 100].map(item => ({
  key: item,
  value: item,
  text: item
})))

const defaultLimit = 15;

const getLoaderContent = (count) => {
  const cards = []
  for (let i = 0; i < count; i++) {
    cards.push(<CardLoader key={i} />)
  }
  return cards
};

class RedditCardsContainer extends React.Component {
    constructor(props) {
        super(props);
        this.fetchComments = this.fetchComments.bind(this);
        this.onChangeLimit = this.onChangeLimit.bind(this);
        this.loadMore = this.loadMore.bind(this);
        this.state = {
          data: [],
          loading: true,
          limit: defaultLimit,
          offset: 0,
        };
    }
    componentDidMount() {
      let params = {
          subreddit_name: "explainlikeimfive",
          limit: this.state.limit,
          offset: this.state.offset,
          subtask_type: this.props.subtask_type
      };
      this.fetchComments(params);
    }
    loadMore() {
      const params = {
        subreddit_name: this.props.subreddit_name,
        subtask_type: this.props.subtask_type,
        limit: this.state.limit,
        offset: this.state.offset,
        prevIds: JSON.stringify(this.state.data.map(item => item.comment_id)),
      };
      this.fetchComments(params);
    }

    fetchComments({ subreddit_name, limit, subtask_type, offset, filters = {}, prevIds = [] }) {
      let url = `${config.webserver_url}/tasks`;
      let params = {
        source: subreddit_name,
        subtask_type,
        limit,
        offset,
        prevIds,
        task_type: 'reddit_classify'
      }
      this.setState({
        loading: true
      })
      axios
        .get(url, { params })
        .then(response => {
          this.setState(((prevState) => ({
              loading: false,
              data: prevState.data.concat(response.data.data)
          })))
        })
        .catch((error) => {
            console.log(error)
        })    
    }

    onChangeLimit(e, selection) {
      e.preventDefault();
      this.setState({
        limit: selection.value
      })
    }
    render() {
        if (this.state.loading === false && this.state.data.length === 0) {
          return (
            <h5 className={'no-cards-container'}>No new comments for now!</h5>
          )
        } else {
            return (
            <div>
            <Card.Group className={'cards-container'}>
            {
                this.state.data.map((item) => <RedditCard
                key={item.unique_id}
                {...item} />)
            }
            {
              this.state.loading && getLoaderContent(this.state.limit)
            }
            </Card.Group>
            <div className="pagination-container">
              <Pagination
                onButtonClick={this.loadMore}
                onChange={this.onChangeLimit}
                value={this.state.limit}
                options={options}
              />
            </div>
          </div>
          )
        }
    }
};

export default withCookies(withRouter(RedditCardsContainer))
