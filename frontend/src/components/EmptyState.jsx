import { Camera } from 'lucide-react';
const EmptyState = ({ onCreate }) => (
  <div className="bg-white/5 backdrop-blur-xl rounded-2xl border border-purple-500/20 p-12 text-center">
    <Camera className="w-16 h-16 text-gray-500 mx-auto mb-4" />
    <h3 className="text-xl font-semibold text-gray-300 mb-2">No posts yet</h3>
    <p className="text-gray-400 mb-6">Be the first to share something!</p>
    <button
      onClick={onCreate}
      className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-2 rounded-full font-semibold hover:shadow-lg hover:shadow-purple-500/50 transition-all"
    >
      Create First Post
    </button>
  </div>
);
export default EmptyState;