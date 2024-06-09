import React, { useState, useEffect } from 'react';
import './Home.css';
import JobComponent from '../components/Job';

function Home() {
  const [searchInput, setSearchInput] = useState("");

  const handleSearchChange = (event) => {
    setSearchInput(event.target.value);
  };

  return (
    <div className="Home">
      <div className="header">
        <h1>Findernship</h1>
        <p>a web scraping application to find summer 25 internships</p>
        </div>
        <div className="table-header">
          <input 
          type="text" 
          placeholder="Search.." 
          value={searchInput}
          onChange={handleSearchChange}
          />
          <button>Sort</button>
        </div>
      <div className="table">
        <JobComponent searchQuery={searchInput}/>
      </div>
    </div>
  );
}

export default Home;