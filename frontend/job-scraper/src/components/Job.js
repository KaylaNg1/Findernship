import React, { useState, useEffect } from 'react';
import './Job.css'

const JobComponent = ({ searchQuery }) => {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/getData');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setData(data);
        setLoading(false);
      } catch (error) {
        setError(error.message);
      }
    };

    fetchData(); // Call fetchData once when the component mounts
  }, []); // Empty dependency array means this effect runs once when the component mounts
  if (loading) {
    return (
      <div className="loading-spinner">
        <div className="spinner"></div>
      </div>
    );
  }

  if (!data.length) {
    return <div>No job postings found.</div>;
  }
  
  const filteredData = data.filter((item) =>
    item.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.position.toLowerCase().includes(searchQuery.toLowerCase()) ||
    item.skills.some(skill => skill.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="JobComponent">
      {filteredData.map(item => (
        <div className="Component">
          <div className="Logo">
            <a href={item.link}><img src={item.logo}></img></a>
          </div>
          <div>
            <h1 className='Company'>{item.company}</h1>
          </div>
          {item.skills.map(skill => (
            <div className="Skills">
              <button className="Skill-Btn">{skill}</button> {/* will need to be a dynamic component */}
            </div>
          ))}
          <div className="Position">
            <h3>{item.position}</h3>
          </div>
          <div className="Description">

          </div>
        </div>
      ))}
    </div>
  );
};

export default JobComponent;