import React from 'react';
import SearchBar from './SearchBar';
import AdvancedSettings from './AdvancedSettings';
import LinkList from './List';
import { Button } from 'semantic-ui-react';
import axios from 'axios';
import { Image, List } from 'semantic-ui-react';
import wiki_logo from '../wiki_logo.png';

class Home extends React.Component {
  state = {
    value: '',
    categories: [],
    loading: false,
    links: [],
    method: 'articles',
    language: 'en',
    filter: 'popularity',
    limit: 10
  };

  renderResults = () => {
    console.log(this.state.links);
    this.state.links.map(link => {
      return (
        <List.Item>
          <Image avatar src={wiki_logo} />
          <List.Content>
            <List.Header>Hi</List.Header>
          </List.Content>
        </List.Item>
        // <List.Item>
        //   <Image avatar src={wiki_logo} />
        //   <List.Content>
        //     <List.Header>link</List.Header>
        //   </List.Content>
        // </List.Item>
      );
    });
  };

  handleResultSelect = (e, { result }) =>
    this.setState({ value: result.title });

  handleSearchBarChange = (e, { value }) => {
    this.setState({ value: value });
    this.autocomplete(e);
  };

  handleMethodSettingsChange = (e, { value }) =>
    this.setState({ method: value, categories: [] });

  handleLanguageSettingsChange = (e, { value }) =>
    this.setState({ language: value });

  handleFilterSettingsChange = (e, { value }) =>
    this.setState({ filter: value });

  handleLimitSettingsChange = (e, { value }) => this.setState({ limit: value });

  query(event) {
    setTimeout(() => {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:5000/',
        data: {
          method: this.state.method,
          query: this.state.value,
          language: this.state.language,
          filter: this.state.filter,
          limit: this.state.limit,
          stub: 'include'
        }
      }).then(response => {
        const links = response.data;
        if (links) {
          links.map(links => {
            this.state.links.push(links);
          });
        }
        this.setState({ links: this.state.links });
      });
    }, 300);
  }

  autocomplete(event) {
    if (this.state.method == 'category') {
      this.setState({ categories: [], loading: true });
      setTimeout(() => {
        axios({
          method: 'post',
          url: 'http://127.0.0.1:5000/category-autocomplete',
          data: {
            language: 'en',
            prefix: this.state.value
          }
        }).then(response => {
          const categories = response.data.categories;

          if (categories) {
            categories.map(category => {
              this.state.categories.push({ title: category });
            });
          }
          this.setState({ loading: false });
        });
      }, 300);
    }
  }

  render() {
    return (
      <div>
        <div className="home">
          <SearchBar
            autocomplete={this.handleSearchBarChange.bind(this)}
            loading={this.state.loading}
            value={this.state.value}
            categories={this.state.categories}
            handleResultSelect={this.handleResultSelect.bind(this)}
          />
          <Button
            id="search-button"
            circular
            color="green"
            icon="search"
            size="large"
            onClick={this.query.bind(this)}
          />
        </div>
        <div className="advanced">
          <AdvancedSettings
            handleMethodSettingsChange={this.handleMethodSettingsChange.bind(
              this
            )}
            handleLanguageSettingsChange={this.handleLanguageSettingsChange.bind(
              this
            )}
            handleFilterSettingsChange={this.handleFilterSettingsChange.bind(
              this
            )}
            handleLimitSettingsChange={this.handleLimitSettingsChange.bind(
              this
            )}
          />
        </div>
        <div className="link-container">
          <List selection verticalAlign="middle">
            {this.renderResults()}
          </List>
        </div>
      </div>
    );
  }
}

export default Home;
