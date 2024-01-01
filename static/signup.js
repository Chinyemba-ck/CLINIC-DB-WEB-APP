// Import Firebase modules (Firebase version 9.17.1)
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-app.js";
import {  createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-auth.js";
import { userSignIn } from "./auth2.js";
// Firebase configuration (replace with your own config)
const firebaseConfig = {
    apiKey: "AIzaSyDWDnJ_WHWTQgOkV7WY_TArMTFDr3gIZuY",
    authDomain: "authpy-e05d3.firebaseapp.com",
    projectId: "authpy-e05d3",
    storageBucket: "authpy-e05d3.appspot.com",
    messagingSenderId: "524320938480",
    appId: "1:524320938480:web:0c31cb6485d43769d12535",
    measurementId: "G-QZCKZDRMW4"
  };


// Initialize Firebase with the provided configuration
const app = initializeApp(firebaseConfig);
const auth = getAuth();


// Get DOM elements
const userEmail = document.getElementById("new-email");
const userPassword = document.getElementById("new-password");
const signUpButton = document.getElementById("sign-up-btn");
const signUpWithGoogle = document.getElementById("sign-up-Google")

// Get DOM element
const googleSignIn = document.getElementById("sign-in-Google");

const userSignUp = async () => {
    // Get user input from form
    const signUpEmail = userEmail.value;
    const signUpPassword = userPassword.value;

    try {
        // Create a new user with the provided email and password
        const userCredential = await createUserWithEmailAndPassword(auth, signUpEmail, signUpPassword);
        const user = userCredential.user;

        // Send the user data to the Flask route /user-data
        const response = await fetch('/user-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user: user }),
        });

        if (response.ok) {
            
            console.log('User data to be sent:', { user: user });
            
            // Redirect to the dashboard route
            window.location.href = '/dashboard';
        } else {
            console.error('Failed to store user data on the server');
        }
    } catch (error) {
        // Handle any errors that occur during the sign-up process
        const errorCode = error.code;
        const errorMessage = error.message;
        console.error(errorCode, errorMessage);
    }
};


// Add event listener to the sign-up button to trigger userSignUp function
signUpButton.addEventListener("click", userSignUp);


signUpWithGoogle.addEventListener("click", function (event) {
   
    event.preventDefault();
    userSignIn();
   
});