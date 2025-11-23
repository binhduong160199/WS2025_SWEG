import React from 'react';
import { TrendingUp } from 'lucide-react';

const Navbar = ({ onCreateClick, searchQuery, setSearchQuery, onSearch }) => (
  <header className="bg-black/40 backdrop-blur-xl border-b border-purple-500/20 sticky top-0 z-50">
    <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
      <div className="flex items-center space-x-2">
        <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
          <TrendingUp className="w-6 h-6 text-white" />
        </div>
        <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
          SocialHub
        </h1>
      </div>
      <div className="flex items-center space-x-4">
        <div className="relative">
          <input
            type="text"
            placeholder="Search posts..."
            value={searchQuery}
            onChange={e => {
              setSearchQuery(e.target.value);
              onSearch(e.target.value); // Run search immediately as you type
            }}
            className="w-64 bg-white/10 border border-purple-500/30 rounded-full px-4 py-2 pl-10 text-white placeholder-gray-400 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20"
          />
        </div>
        <button
          onClick={onCreateClick}
          className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-2 rounded-full font-semibold hover:shadow-lg hover:shadow-purple-500/50 transition-all duration-300 flex items-center space-x-2"
        >
          <span>Create Post</span>
        </button>
      </div>
    </div>
  </header>
);

export default Navbar;