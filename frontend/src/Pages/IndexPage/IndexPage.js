import React from 'react';
import './IndexPage.css';
import { Grid } from 'semantic-ui-react'
import Header from '../../Components/Header'
import GetToxicity from '../../Components/GetToxicity'

import './IndexPage.css'
import RedditCardContainer from '../../Components/RedditCardContainer';
import { TOXIC_HL } from '../../constants';

const IndexPage = (props) => {
    return (
      <div className="App">
        <Header showBackButton={false} />
        <div className="container-index">
          <Grid>
            <Grid.Column width={11}>
            <RedditCardContainer
              limit={10}
              subtask_type={TOXIC_HL}
            />
            </Grid.Column>
            <Grid.Column width={5}>
              <GetToxicity />
            </Grid.Column>
          </Grid>
        </div>
      </div>
    )
}

export default IndexPage;
