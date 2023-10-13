import '../styles/headerStyle.css';

function Header() {
    return (
        <nav className="navbar">
            <a href="#home" className="nav-item">Home</a>
            <a href="#about-us" className="nav-item">About Us</a>
            <a href="#contact-us" className="nav-item">Contact Us</a>
            <a href="#mission" className="nav-item">Mission</a>
        </nav>
    )
}
export default Header;