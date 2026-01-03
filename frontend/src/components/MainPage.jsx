import React, { useState, useEffect, useRef } from 'react';
import debounce from 'lodash.debounce';
import { Smile, Frown, Filter } from 'lucide-react';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import PostCard from './PostCard';
import CreatePostModal from './CreatePostModal';
import LoadingSpinner from './LoadingSpinner';
import EmptyState from './EmptyState';
import Footer from './Footer';
import StatsCard from './StatsCard';
import { usePosts } from '../contexts/PostContext';

const Snackbar = ({ message, onClose }) => (
  <div className="fixed top-6 left-1/2 -translate-x-1/2 bg-green-500 text-white px-6 py-3 rounded-full shadow-lg z-[100] animate-fadeIn">
    {message}
    <button onClick={onClose} className="ml-4 font-bold">×</button>
  </div>
);

const MainPage = () => {
  const { posts, loading, error, addPost, doSearch } = usePosts();
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredPosts, setFilteredPosts] = useState(null); 
  const [showSuccess, setShowSuccess] = useState(false);
  const [sentimentFilter, setSentimentFilter] = useState('all'); // NEW: sentiment filter

  const [activeTab, setActiveTab] = useState('feed');
  const debouncedSearchRef = useRef(null);

  useEffect(() => {
    debouncedSearchRef.current = debounce(async (value) => {
      if (!value.trim()) {
        setFilteredPosts(null);
        return;
      }
      try {
        const results = await doSearch(value);
        setFilteredPosts(results);
      } catch (err) {
        console.error('Search failed:', err);
        setFilteredPosts([]);
      }
    }, 400);

    return () => {
      if (debouncedSearchRef.current && debouncedSearchRef.current.cancel) {
        debouncedSearchRef.current.cancel();
      }
    };
  }, [doSearch]);

  const handleSearch = (value) => {
    setSearchQuery(value);
    if (debouncedSearchRef.current) debouncedSearchRef.current(value);
  };

  const handleCreate = async (newPost) => {
    await addPost(newPost);
    setShowCreateModal(false);
    setShowSuccess(true);
    setTimeout(() => setShowSuccess(false), 2500);
    setFilteredPosts(null);
    setSearchQuery('');
  };

  const handleLike = (postId) => {
    // Liking logic (optional)
  };

  // Filter posts by sentiment
  const filterBySentiment = (postsToFilter) => {
    if (sentimentFilter === 'all') return postsToFilter;
    return postsToFilter.filter(post => 
      post.sentiment_label && post.sentiment_label.toUpperCase() === sentimentFilter.toUpperCase()
    );
  };

  const displayPosts = filterBySentiment(filteredPosts !== null ? filteredPosts : posts);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex flex-col">
      {showSuccess && <Snackbar message="Post created successfully!" onClose={() => setShowSuccess(false)} />}

      <Navbar
        onCreateClick={() => setShowCreateModal(true)}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        onSearch={handleSearch}
      />
            
            {/* ---------------- SENTIMENT FILTER BUTTONS ---------------- */}
            {!loading && posts.length > 0 && (
              <div className="mb-6 flex items-center space-x-3 bg-white/5 backdrop-blur-xl rounded-xl p-4 border border-purple-500/20">
                <Filter className="w-5 h-5 text-purple-400" />
                <span className="text-sm text-gray-300 font-medium">Filter by Sentiment:</span>
                
                <button
                  onClick={() => setSentimentFilter('all')}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                    sentimentFilter === 'all'
                      ? 'bg-purple-500 text-white'
                      : 'bg-white/5 text-gray-300 hover:bg-white/10'
                  }`}
                >
                  All Posts
                </button>
                
                <button
                  onClick={() => setSentimentFilter('positive')}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                    sentimentFilter === 'positive'
                      ? 'bg-green-500 text-white'
                      : 'bg-white/5 text-gray-300 hover:bg-white/10'
                  }`}
                >
                  <Smile className="w-4 h-4" />
                  <span>Positive</span>
                </button>
                
                <button
                  onClick={() => setSentimentFilter('negative')}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                    sentimentFilter === 'negative'
                      ? 'bg-red-500 text-white'
                      : 'bg-white/5 text-gray-300 hover:bg-white/10'
                  }`}
                >
                  <Frown className="w-4 h-4" />
                  <span>Negative</span>
                </button>
              </div>
            )}
            
      <main className="flex-1 max-w-6xl mx-auto px-4 py-8 w-full">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1">
            <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} postsCount={displayPosts.length} onFeedClick={() => setFilteredPosts(null)} />
          </div>
          <div className="lg:col-span-2">
            {error && <div>{error}</div>}
            {!loading && displayPosts.length > 0 && <StatsCard />}
            {loading ? (
              <LoadingSpinner />
            ) : displayPosts.length === 0 ? (
              <EmptyState onCreate={() => setShowCreateModal(true)} />
            ) : (
              <div className="space-y-6">
                {displayPosts.map((post, index) => (
                  <PostCard key={post.id} post={post} onLike={handleLike} isLatest={index === 0 && !searchQuery} />
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
      <Footer />
      {showCreateModal && <CreatePostModal onClose={() => setShowCreateModal(false)} onSubmit={handleCreate} />}
    </div>
  );
};

export default MainPage;