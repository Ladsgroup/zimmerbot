import React from 'react';
import SearchBar from './SearchBar';
import AdvancedSettings from './AdvancedSettings';
import LinkList from './List';
import { Button, Checkbox } from 'semantic-ui-react';
import axios from 'axios';
import { Image, List } from 'semantic-ui-react';
import wiki_logo from '../wiki_logo.png';

class Home extends React.Component {
  state = {
    value: '',
    categories: [],
    loading: false,
    links: [],
    method: 'individual',
    language: 'en',
    filter: 'popularity',
    limit: 10,
    checked: [],
    more_info: 'Filters by popularity score.'
  };

  renderResults = () => {
    this.state.links.map(link => {
      return (
        <List.Item>
          <Image avatar src={wiki_logo} />
          <List.Content>
            <List.Header>Hi</List.Header>
          </List.Content>
        </List.Item>
      );
    });
  };
  
  handleCheck = (id) => {
    var checked = this.state.checked;
    checked[id] = !checked[id];
    this.setState({ checked: checked});
  }
    
    
  handleCheckAll = () => {
    var checks = [];
    for (var i =0; i<this.state.links.length; i++) {
      checks.push(true);
    }
    this.setState({ checked: checks });
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

  handleFilterSettingsChange = (e, { value }) => {
    if (value === "ores_quality") {
      this.setState({more_info: "Filters by ORES assessment score"});
    } else if (value === "popularity") {
      this.setState({more_info: "Filters by popularity score"});
    } else if (value === "most_linked_to") {
      this.setState({more_info: "Related articles on the same page"});
    }
    this.setState({ filter: value });
  }

  handleLimitSettingsChange = (e, { value }) => this.setState({ limit: value });

  query(event) {
    setTimeout(() => {
      axios({
        method: 'post',
        url: 'http://zimmerbot.host/',
        data: {
          method: this.state.method,
          query: this.state.value,
          language: this.state.language,
          filter: this.state.filter,
          limit: parseInt(this.state.limit),
          stub: 'include'
        }
      }).then(response => {
        const links = response.data;
        console.log(links);
        if (links) {
          if (
            links[0] === 'No search results found for this query' &&
            this.state.method === 'category'
          ) {
            alert("Category '" + this.state.value + "' not found.");
          } else {
            links.map(links => {
              this.state.links.push(links);
            });
            
            // Sets state for checkboxes
            var checks = [];
            for (var i =0; i<this.state.links.length; i++) {
              checks.push(false);
            }
            this.setState({ checked: checks });
          }
        }
        this.setState({ links: this.state.links });
      });
    }, 300);
  }

  autocomplete(event) {
    if (this.state.method === 'category') {
      this.setState({ categories: [], loading: true });
      setTimeout(() => {
        axios({
          method: 'post',
          url: 'http://zimmerbot.host/category-autocomplete',
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
            more_info={this.state.more_info}
          />
        </div>
        {this.state.links.length > 0 ? (
          <div className="link-container">
            <div className="ui toggle button" onClick={this.handleCheckAll.bind(this)}>Select All</div>
          </div>
        ) : (<div></div>)}
        
        
        <div className="link-container">
          <div className="ui raised segments">
            {this.state.links.map(function(listValue, id) {
              return (
                <div className="ui segment">
                  <div className="ui checkbox">
                    <Checkbox name="select" checked={this.state.checked[id]} onChange={this.handleCheck.bind(this, id)}/>
                  </div>
                  <a href={listValue}>
                    {listValue}
                  </a>
                </div>
              );
            }, this)}
          </div>
        </div>
      </div>
    );
  }
}

export default Home;
