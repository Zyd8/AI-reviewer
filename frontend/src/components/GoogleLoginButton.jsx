import React, {useState} from 'react';
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import './GoogleLoginButton.css'

const GoogleLoginButton = () => {

  const [user, setUser] = useState(null);

  const responseGoogle = async (response) => {
    console.log(response);
    // Send the token to the backend for verification
    try {
      const res = await fetch('http://localhost:5000/auth', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: response.credential }),
      });
      const data = await res.json();
      console.log(data);  // Log the response from the backend
      setUser(data);
    } catch (error) {
      console.error('Error verifying token:', error);
    }
  };

  return (
    <GoogleOAuthProvider clientId={process.env.GOOGLE_CLIENT_ID}>
        {user ? (
          <div className="user-info">
            <h2>Welcome, {user.name}!</h2>
            <img src={user.imageUrl} alt={user.name} />
          </div>
        ) : (
          <GoogleLogin
            onSuccess={responseGoogle}
            onError={responseGoogle}
            className="google-login-button"
          />
        )}
    </GoogleOAuthProvider>
  );
};

export default GoogleLoginButton;