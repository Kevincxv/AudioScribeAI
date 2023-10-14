import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ContactUs from './components/ContactUs';
import Demo from './components/DemoIndex';
import Home from './components/Home';
import AboutUs from './components/AboutUs';
import DemoPost from './components/DemoPost';

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/demo" element={<Demo />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;