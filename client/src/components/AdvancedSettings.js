import React from 'react';
import { Form, Popup, Button, Icon } from 'semantic-ui-react';

const search = [
  // { key: 'articles', text: 'Articles', value: 'articles' },
  // { key: 'categories', text: 'Categories', value: 'categories' }
  { key: 'individual', text: 'Articles', value: 'individual' },
  { key: 'category', text: 'Category', value: 'category' },
  { key: 'related', text: 'Related Articles', value: 'related' },
  { key: 'linked', text: 'Linked To', value: 'linked' },
  // { key: 'page_links', text: 'Linked From', value: 'page_links' }
];

const language = [
  { key: 'english', text: 'English', value: 'en' },
  { key: 'spanish', text: 'Spanish', value: 'es' }
];

const filter = [
  { key: 'popularity', text: 'Popularity', value: 'popularity' },
  { key: 'quality', text: 'Quality', value: 'ores_quality' },
  { key: 'linked', text: 'Linked To', value: 'most_linked_to' }
  // { key: 'score', text: 'Article Score', value: 'score' }
];

const limit = [
  { key: 'number', text: 'Number of Articles', value: 'number' },
  { key: 'size', text: 'Size (in MB)', value: 'size' }
];

class AdvancedSettings extends React.Component {
  state = {};

  handleChange = (e, { value }) => this.setState({ value });

  test() {
    alert(this.state.value);
  }

  render() {
    const { value } = this.state;
    return (
      <div>
        <h1>Advanced Settings</h1>
        <hr />
        <br />
        <Form size="massive">
          <Form.Group widths={16}>
            <Form.Select
              fluid
              label="Search For"
              options={search}
              onChange={this.props.handleMethodSettingsChange}
              placeholder="Articles"
            />
            <Form.Select
              fluid
              label="Language"
              options={language}
              onChange={this.props.handleLanguageSettingsChange}
              placeholder="English"
            />
          </Form.Group>

          <Form.Group widths="equal">
          <Form.Select
            fluid
            label={<label> Filter By <Popup
              trigger={<Icon name='info circle small' />}
              content={this.props.more_info}
              basic
            /></label>}
            options={filter}
            onChange={this.props.handleFilterSettingsChange}
            placeholder="Popularity"
          />
          <Form.Input
            fluid
            label={<label> Limit <Popup
              trigger={<Icon name='info circle small' />}
              content="Number of links generated."
              basic
            /></label>}
            type="number"
            onChange={this.props.handleLimitSettingsChange}
            placeholder="10"
          />
          </Form.Group>
        </Form>
      </div>
    );
  }
}

// <Form.Select
//   fluid
//   label="Limit By"
//   options={limit}
//   onChange={this.props.handleLimitSettingsChange}
//   placeholder="Number of Articles"
// />

export default AdvancedSettings;
