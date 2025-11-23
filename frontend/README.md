# SocialHub Frontend

A modern, dark-themed social media dashboard built with React and Tailwind CSS. SocialHub features a glassmorphism UI, real-time post searching, and an interactive analytics dashboard.

## Features

* **Create Posts:** Share updates with text and image support (Base64 encoding).
* **Real-time Search:** Debounced search functionality to filter posts instantly as you type.
* **Analytics Dashboard:** Visual stats card displaying Total Posts, Active Users, Likes, and Comments.
* **Interactive Feedback:** Loading spinners, empty states, and snackbar notifications for successful actions.

## Tech Stack

* **Core:** React 18
* **Styling:** Tailwind CSS (v3)
* **Icons:** Lucide React
* **State Management:** React Context API (`PostsProvider`)
* **HTTP Client:** Native Fetch API

## Getting Started

### Prerequisites
* Node.js (v14 or higher)
* npm or yarn

### Installation

1.  **Install dependencies:**
    ```bash
    npm install
    ```
    *(Note: This automatically installs Tailwind CSS, PostCSS, and Autoprefixer).*

2.  **Start the development server:**
    ```bash
    npm start
    ```

The application will run on [http://localhost:3000](http://localhost:3000).

## Configuration

The frontend is configured to communicate with a backend server.

**Update API Endpoint:**
If your backend is running on a port other than `5001`, update the base URL in the constants file:

1.  [cite_start]Open `src/utils/constants.js`[cite: 526].
2.  Modify the `API_BASE_URL` variable:

```javascript
// src/utils/constants.js
export const API_BASE_URL = 'http://localhost:5001/api'; // Change port if needed

## Project Structure
frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── CreatePostModal.jsx   # Post creation form with image upload
│   │   ├── LatestPostSpotlight.jsx # Featured latest post component
│   │   ├── Navbar.jsx            # Top navigation and search bar
│   │   ├── PostCard.jsx          # Individual post display with likes
│   │   ├── Sidebar.jsx           # Navigation and mini-stats
│   │   └── StatsCard.jsx         # Dashboard metrics (Likes, Users, etc.)
│   ├── contexts/
│   │   └── PostContext.js        # Global state for posts and fetching
│   ├── services/
│   │   └── api.js                # API endpoints (GET, POST, Search)
│   ├── utils/
│   │   └── constants.js          # App configuration
│   ├── App.js                    # Main layout and logic
│   ├── index.css                 # Tailwind directives and global styles
│   └── index.js                  # Entry point
├── postcss.config.js             # PostCSS configuration
├── tailwind.config.js            # Tailwind configuration
└── README.md