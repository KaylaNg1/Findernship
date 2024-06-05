import React from 'react';
import { Routes, Route} from "react-router-dom";
import './Home.css';
import JobComponent from '../components/Job';

function Home() {
  return (
    <div className="Home">
      <div className = "header">
        <h1>Summer 25 SWE Internships</h1>
      </div>
      <div className = "table-header">
        <input type="text" placeholder="Search.."/>
        <button>Sort</button>
      </div>
      <div className = "table">
        <JobComponent/>
      </div>
    </div>
  );
}

export default Home;