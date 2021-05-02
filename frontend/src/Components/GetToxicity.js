import React from 'react'
import { Button, Form, Header, Label, Icon } from 'semantic-ui-react'
import axios from 'axios';
import config from '../config';

class GetToxicity extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      text: '',
      toxicity_text: '',
      color: '',
      loading: false
    };
    this.onTextChange = this.onTextChange.bind(this);
    this.onGetToxicityClick = this.onGetToxicityClick.bind(this);
    this.urlString = `${config.webserver_url}/classify`;
  }
  onTextChange (event) {
    this.setState({
      text: event.target.value
    });
  }
  onGetToxicityClick() {
    let text = this.state.text;
    if (text && text.trim() && text.trim().length > 0) {
      this.setState({
        loading: true,
        toxicity_text: ''
      });  
      let params = {
        'text': text.trim()
      }
      axios
        .get(this.urlString, { params })
        .then(response => {
          let toxicity_text = 'You are not the asshole';
          let color = 'green';
          if (response.data.predicted_label === 1) {
            toxicity_text = 'You are the asshole';
            color = 'red';
          } else if (response.data.predicted_label === 2) {
            toxicity_text = 'Everyone sucks here';
            color = 'red';
          } else if (response.data.predicted_label === 3) {
            toxicity_text = 'No assholes here';
            color = 'red';
          }
          this.setState({
            toxicity_text,
            color,
            loading: false
          })
        });
    }
  }
  render() {
   return (
    <Form>
      <Header as='h2'>
        <Icon name='binoculars' />
        <Header.Content>
          Curious?
          <Header.Subheader>Try it yourself!</Header.Subheader>
        </Header.Content>
      </Header>
      <Form.TextArea onChange={this.onTextChange} value={this.state.text} placeholder={"Type in the text you want to check"}/>
      <Button content='AmITheAsshole?' onClick={this.onGetToxicityClick} loading={this.state.loading}/>
      {this.state.toxicity_text && <Label as='a' color={this.state.color} tag>
        {this.state.toxicity_text}
      </Label>}
    </Form>
    )
  }
}

export default GetToxicity;
