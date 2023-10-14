import React, { useState, useEffect  } from 'react';
import Home from './Home';
import AboutUs from './AboutUs';
import ContactUs from './ContactUs';
import EmployeeForm from './EmployeeForm';
// import './index.css';

function FrontPage() {

  const [showEmployeeForm, setShowEmployeeForm] = useState(false);

  const handleEmployeeClick = () => {
    setShowEmployeeForm(true);
  };

  return (
    <div className="App">
      {showEmployeeForm ? (
        <EmployeeForm />
      ) : (
        <>
          <Home />
          <AboutUs />
          <ContactUs onEmployeeClick={handleEmployeeClick} />
        </>
      )}
    </div>
  );
}

export default FrontPage;
