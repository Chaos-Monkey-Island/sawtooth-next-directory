/* Copyright 2019 Contributors to Hyperledger Sawtooth

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
----------------------------------------------------------------------------- */


import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Card, Grid } from 'semantic-ui-react';


import './Manage.css';
import People from 'containers/approver/people/People';
import TrackHeader from 'components/layouts/TrackHeader';


/**
 *
 * @class         Manage
 * @description   Manage component
 *
 */
class Manage extends Component {

  /**
   * Render content
   * @returns {JSX}
   */
  renderContent () {
    const disabled = process.env.REACT_APP_ENABLE_LDAP_SYNC === '1' ?
      'disabled' : '';
    return (
      <div id='next-approver-manage-content' className='next-ease'>
        <Grid doubling stackable>
          <Grid.Row columns={3} stretched>
            <Grid.Column>
              <Card
                id='next-approver-manage-packs-card'
                fluid
                as={Link}
                to='manage/packs'
                header='Packs'
                className='minimal huge'
                description={`
                  Create, modify, or delete an existing pack.
                `}/>
            </Grid.Column>
            <Grid.Column>
              <Card
                id='next-approver-manage-roles-card'
                as={process.env.REACT_APP_ENABLE_LDAP_SYNC === '1' ?
                  '' : Link}
                fluid
                to='manage/roles'
                header='Roles'
                className={`minimal huge ${disabled}`}
                description={`
                  Create a new role, modify an existing one,
                  or delete one.
                `}/>
            </Grid.Column>
            <Grid.Column>
              <Card
                id='next-approver-manage-delegations-card'
                fluid
                header='Delegations'
                className='minimal huge disabled'
                description={`
                  Setup or modify a temporary or permanent delegation.
                `}/>
            </Grid.Column>
          </Grid.Row>
          <Grid.Row columns={3} stretched>
            <Grid.Column>
              <Card
                id='next-approver-manage-hierarchical-card'
                fluid
                header='Hierarchical'
                className='minimal huge disabled'
                description={`
                  Setup who can approve on your behalf.
                `}/>
            </Grid.Column>
            <Grid.Column>
              <Card
                id='next-approver-manage-alerts-card'
                fluid
                header='Alerts'
                className='minimal huge disabled'
                description={`
                  Manage what you get alerts for and alert frequency.
                `}/>
            </Grid.Column>
            <Grid.Column>
            </Grid.Column>
          </Grid.Row>
        </Grid>
        <Card.Group itemsPerRow={3}>
        </Card.Group>
      </div>
    );
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { showSearch } = this.props;
    return (
      <div>
        { showSearch && <People {...this.props}/> }
        { !showSearch &&
          <Grid id='next-approver-grid'>
            <Grid.Column
              id='next-approver-grid-track-column'
              width={16}>
              <TrackHeader
                title='Manage'
                {...this.props}/>
              { this.renderContent() }
            </Grid.Column>
          </Grid>
        }
      </div>
    );
  }

}


export default Manage;
