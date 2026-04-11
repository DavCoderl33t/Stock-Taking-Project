import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./app.css"; // Global styles for the application

// Create a React root and mount the application into the DOM element with id="root"
// This is typically defined in index.html
ReactDOM.createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        {/* 
          StrictMode is a development-only tool:
          - Helps identify unsafe lifecycle usage
          - Detects unexpected side effects
          - May intentionally double-invoke certain functions in dev (not production)
        */}
        <App />
    </React.StrictMode>
);