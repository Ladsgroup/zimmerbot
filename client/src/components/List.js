import React from 'react';
import { Image, List } from 'semantic-ui-react';
import wiki_logo from '../wiki_logo.png';

const LinkList = () => (
  <List.Item>
    <Image avatar src={wiki_logo} />
    <List.Content>
      <List.Header>{this.props.link}</List.Header>
    </List.Content>
  </List.Item>
);

export default LinkList;
