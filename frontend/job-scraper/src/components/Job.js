import React, { useState, useEffect } from 'react';
import './Job.css'

const JobComponent = () => {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/getData');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setData(data);
      } catch (error) {
        setError(error.message);
      }
    };

    fetchData(); // Call fetchData once when the component mounts
  }, []); // Empty dependency array means this effect runs once when the component mounts
  if (!data) {
    return <div>Loading...</div>;
  }
  return (
    <div className="JobComponent">
      {data.map(item => (
        <div className="Component">
          <div className="Logo">
            <a href={item.link}><img src={item.logo}></img></a>
          </div>
          <div>
            <h1 className='Company'>{item.company}</h1>
          </div>
          {item.skills.map(skill => (
            <div className="Skills">
            <button>{skill}</button> {/* will need to be a dynamic component */}
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