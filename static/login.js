// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.0.0/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.0.0/firebase-auth.js";

// Add your own Firebase config here
const firebaseConfig = {
  apiKey: "AIzaSyDWDnJ_WHWTQgOkV7WY_TArMTFDr3gIZuY",
  authDomain: "authpy-e05d3.firebaseapp.com",
  projectId: "authpy-e05d3",
  storageBucket: "authpy-e05d3.appspot.com",
  messagingSenderId: "524320938480",
  appId: "1:524320938480:web:0c31cb6485d43769d12535",
  measurementId: "G-QZCKZDRMW4"
};


// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth();
const provider = new GoogleAuthProvider();

// Get DOM element
const googleSignIn = document.getElementById("sign-in-Google");



// Function to sign in with Google
const userSignIn = async () => {
  try {
    const result = await signInWithPopup(auth, provider);
    const user = result.user;

    // Store user data in Flask session
    const response = await fetch('/user-data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user: user }),
    });

    if (response.ok) {
      console.log('User data stored successfully'); // Check if this message appears in the console
      // Redirect to the dashboard route
      window.location.href = '/dashboard';
    } else {
      console.error('Failed to store user data on the server');
    }
  } catch (error) {
    // Handle sign-in errors
    const errorCode = error.code;
    const errorMessage = error.message;
    console.log(errorCode, errorMessage);
  }
};



// Add event listener
googleSignIn.addEventListener('click', userSignIn);


export { userSignIn };