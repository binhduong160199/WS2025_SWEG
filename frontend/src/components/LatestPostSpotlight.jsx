import { Sparkles, Clock } from 'lucide-react';
import { usePosts } from '../contexts/PostContext';

const LatestPostSpotlight = ({ onPostClick }) => {
  const { posts, loading } = usePosts();
  const latestPost = posts && posts.length > 0 ? posts[0] : null;

  if (loading || !latestPost) return null;

  return (
    <div className="mb-8 bg-gradient-to-r from-purple-500/20 to-pink-500/20 backdrop-blur-xl rounded-2xl border border-purple-500/30 p-6 animate-fadeIn">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-5 h-5 text-yellow-400 animate-pulse" />
          <h2 className="text-lg font-bold text-white">Latest from Community</h2>
        </div>
        <div className="flex items-center space-x-2 text-sm text-gray-400">
          <Clock className="w-4 h-4" />
          <span>Just now</span>
        </div>
      </div>
      
      <div className="bg-black/20 rounded-xl p-4">
        <p className="text-white font-semibold mb-2">@{latestPost.user}</p>
        <p className="text-gray-300 line-clamp-2">{latestPost.text}</p>
      </div>
    </div>
  );
};

export default LatestPostSpotlight;