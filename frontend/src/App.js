import React, { useState, useEffect } from 'react';
import debounce from 'lodash.debounce';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import PostCard from './components/PostCard';
import CreatePostModal from './components/CreatePostModal';
import LoadingSpinner from './components/LoadingSpinner';
import EmptyState from './components/EmptyState';
import Footer from './components/Footer';
import StatsCard from './components/StatsCard';
import { PostsProvider, usePosts } from './contexts/PostContext';

const Snackbar = ({ message, onClose }) => (
  <div className="fixed top-6 left-1/2 -translate-x-1/2 bg-green-500 text-white px-6 py-3 rounded-full shadow-lg z-[100] animate-fadeIn">
    {message}
    <button onClick={onClose} className="ml-4 font-bold">×</button>
  </div>
);

const AppContent = () => {
  const { posts, loading, error, addPost, doSearch } = usePosts();
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredPosts, setFilteredPosts] = useState(null); // for search results
  const [showSuccess, setShowSuccess] = useState(false);

  const [activeTab, setActiveTab] = useState('feed');

  const debouncedSearchRef = React.useRef(null);

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

  // This handler triggers when user types
  const handleSearch = (value) => {
    setSearchQuery(value);
    if (debouncedSearchRef.current) debouncedSearchRef.current(value);
  };

  const handleCreate = async (newPost) => {
    await addPost(newPost);
    setShowCreateModal(false);
    setShowSuccess(true);
    setTimeout(() => setShowSuccess(false), 2500);
    setFilteredPosts(null); // Reset search so new post appears
    setSearchQuery('');     // Optional: clear search box after post
  };

  const handleLike = (postId) => {
    // Liking logic (optional)
  };

  // Show posts: filtered if search active, else all
  const displayPosts = filteredPosts !== null ? filteredPosts : posts;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 flex flex-col">
      {showSuccess && <Snackbar message="Post created successfully!" onClose={() => setShowSuccess(false)} />}

      <Navbar
        onCreateClick={() => setShowCreateModal(true)}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        onSearch={handleSearch}
      />
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

const App = () => (
  <PostsProvider>
    <AppContent />
  </PostsProvider>
);

export default App;