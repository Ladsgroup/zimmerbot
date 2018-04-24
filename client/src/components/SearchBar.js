import React from 'react';
import { Search } from 'semantic-ui-react';
import axios from 'axios';

class SearchBar extends React.Component {
  render() {
    return (
      <div className="searchbar">
        <Search
          size="massive"
          icon=""
          loading={this.props.loading}
          showNoResults={false}
          onSearchChange={this.props.autocomplete}
          onResultSelect={this.props.handleResultSelect}
          results={this.props.categories}
          value={this.props.value}
        />
      </div>
    );
  }
}

export default SearchBar;
