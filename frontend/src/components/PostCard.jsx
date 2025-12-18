import React, { useState } from 'react';
import {
  Heart,
  MessageCircle,
  Share2,
  User,
  Eye,
  TrendingUp,
  X
} from 'lucide-react';
import { fetchPostDetail } from '../services/api';

const PostCard = ({ post, onLike, isLatest = false }) => {

  const [liked, setLiked] = useState(false);
  const [likeCount, setLikeCount] = useState(Math.floor(Math.random() * 50));
  const [views] = useState(Math.floor(Math.random() * 200) + 10);

  // NEW: full image modal state
  const [fullImage, setFullImage] = useState(null);
  const [loadingFull, setLoadingFull] = useState(false);

  const handleLike = () => {
    setLiked(!liked);
    setLikeCount(prev => liked ? prev - 1 : prev + 1);
    if (onLike) onLike(post.id);
  };

  const handleThumbnailClick = async () => {
    if (!post.has_image || loadingFull) return;

    try {
      setLoadingFull(true);
      const detail = await fetchPostDetail(post.id);
      setFullImage(detail.image || null);
    } catch (err) {
      console.error('Failed to load full image', err);
    } finally {
      setLoadingFull(false);
    }
  };

  const getAvatarGradient = (username) => {
    const gradients = [
      'from-purple-500 to-pink-500',
      'from-blue-500 to-cyan-500',
      'from-green-500 to-emerald-500',
      'from-orange-500 to-red-500',
      'from-indigo-500 to-purple-500',
    ];
    const index = username.charCodeAt(0) % gradients.length;
    return gradients[index];
  };

  return (
    <>
      <article
        className={`bg-white/5 backdrop-blur-xl rounded-2xl border overflow-hidden transition-all duration-300
        ${isLatest
          ? 'border-yellow-500/50 shadow-lg shadow-yellow-500/20 animate-pulse-slow'
          : 'border-purple-500/20 hover:border-purple-500/40'}
        hover:scale-[1.02] hover:shadow-2xl hover:shadow-purple-500/10`}
      >
        {isLatest && (
          <div className="bg-gradient-to-r from-yellow-500 to-orange-500 px-4 py-2 flex items-center space-x-2">
            <TrendingUp className="w-4 h-4 text-white animate-bounce" />
            <span className="text-sm font-bold text-white">Latest Post</span>
          </div>
        )}

        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <div
                className={`w-12 h-12 bg-gradient-to-r ${getAvatarGradient(post.user)}
                rounded-full flex items-center justify-center ring-2 ring-purple-500/30`}
              >
                <User className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="font-semibold text-white flex items-center space-x-2">
                  <span>{post.user}</span>
                  {post.id % 5 === 0 && (
                    <span className="text-xs bg-purple-500 px-2 py-0.5 rounded-full">
                      Pro
                    </span>
                  )}
                </h3>
                <p className="text-sm text-gray-400">{post.created_at}</p>
              </div>
            </div>
            <div className="flex items-center space-x-2 text-gray-400">
              <Eye className="w-4 h-4" />
              <span className="text-sm">{views}</span>
            </div>
          </div>

          <p className="text-gray-200 mb-4 leading-relaxed">{post.text}</p>

          {/* ---------------- IMAGE SECTION (FIXED) ---------------- */}

          {/* Thumbnail available */}
          {post.image_thumb && (
            <div
              className="mb-4 rounded-xl overflow-hidden bg-black/20 group cursor-pointer"
              onClick={handleThumbnailClick}
            >
              <img
                src={`data:image/jpeg;base64,${post.image_thumb}`}
                alt="Thumbnail"
                className="w-full h-auto object-cover transition-transform duration-300 group-hover:scale-105"
              />
              {loadingFull && (
                <div className="absolute inset-0 bg-black/60 flex items-center justify-center text-white text-sm">
                  Loading...
                </div>
              )}
            </div>
          )}

          {/* Image exists but thumbnail not ready yet */}
          {post.has_image && !post.image_thumb && (
            <div className="mb-4 p-6 text-center text-gray-400 bg-black/20 rounded-xl">
              Image is processing...
            </div>
          )}

          <div className="flex items-center space-x-6 py-3 border-t border-b border-purple-500/20 mb-4">
            <span className="text-sm text-gray-400">{likeCount} likes</span>
            <span className="text-sm text-gray-400">
              {Math.floor(Math.random() * 20)} comments
            </span>
            <span className="text-sm text-gray-400">
              {Math.floor(Math.random() * 10)} shares
            </span>
          </div>

          <div className="flex items-center space-x-6">
            <button
              onClick={handleLike}
              className={`flex items-center space-x-2 transition-all
              ${liked
                ? 'text-pink-500 scale-110'
                : 'text-gray-400 hover:text-pink-500'}`}
            >
              <Heart className={`w-5 h-5 ${liked ? 'fill-pink-500' : ''}`} />
              <span className="text-sm font-medium">Like</span>
            </button>

            <button className="flex items-center space-x-2 text-gray-400 hover:text-blue-500 transition-colors">
              <MessageCircle className="w-5 h-5" />
              <span className="text-sm font-medium">Comment</span>
            </button>

            <button className="flex items-center space-x-2 text-gray-400 hover:text-green-500 transition-colors">
              <Share2 className="w-5 h-5" />
              <span className="text-sm font-medium">Share</span>
            </button>
          </div>
        </div>
      </article>

      {/* ---------------- FULL IMAGE MODAL ---------------- */}
      {fullImage && (
        <div
          className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center"
          onClick={() => setFullImage(null)}
        >
          <div className="relative max-w-4xl max-h-[90vh]">
            <button
              className="absolute -top-10 right-0 text-white hover:text-red-400"
              onClick={() => setFullImage(null)}
            >
              <X className="w-6 h-6" />
            </button>
            <img
              src={`data:image/jpeg;base64,${fullImage}`}
              alt="Full"
              className="rounded-xl max-h-[90vh]"
            />
          </div>
        </div>
      )}
    </>
  );
};

export default PostCard;