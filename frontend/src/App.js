import './App.css';
import FileUpload from './components/FileUpload';
import GoogleLoginButton from './components/GoogleLoginButton';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to My App</h1>
        <div className="components-container">
          <GoogleLoginButton />
          <FileUpload />
        </div>
      </header>
    </div>
  );
}

export default App;
