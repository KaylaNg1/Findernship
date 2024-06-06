import React from 'react';
import { Routes, Route } from "react-router-dom";
import './Home.css';
import JobComponent from '../components/Job';

function Home() {
  return (
    <div className="Home">
      <div className="header">
        <h1>Findernship</h1>
        <p>a web scraping application to find summer 25 internships</p>
        </div>
        <div className="table-header">
          <input type="text" placeholder="Search.." />
          <button>Sort</button>
        </div>
      <div className="table">
        <JobComponent />
      </div>
    </div>
  );
}

export default Home;