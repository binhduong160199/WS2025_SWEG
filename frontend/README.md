```markdown
# Social Media Frontend

## Installation

1. Install dependencies:
```bash
npm install
```

2. Install Tailwind CSS:
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

3. Start the development server:
```bash
npm start
```

The app will run on [http://localhost:3000](http://localhost:3000)

## Backend Setup

Make sure your Flask backend is running on port 5000:

```bash
cd ../backend
python run.py
```

## Technologies Used

- React 18
- Tailwind CSS
- Lucide React (icons)
- Fetch API for HTTP requests

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── App.js          # Main component
│   ├── index.js        # Entry point
│   └── index.css       # Global styles
├── package.json
├── tailwind.config.js
└── README.md
```

## API Configuration

The frontend connects to the backend at `http://localhost:5000/api`. 
If your backend runs on a different port, update the `API_BASE_URL` in `src/App.js`.

## Build for Production

```bash
npm run build
```
