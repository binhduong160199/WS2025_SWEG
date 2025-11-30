import React, { useState, useEffect, useRef } from 'react';
import debounce from 'lodash.debounce';
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

export default MainPage;