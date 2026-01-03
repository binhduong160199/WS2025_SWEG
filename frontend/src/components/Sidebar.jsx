import { TrendingUp } from 'lucide-react';

const Sidebar = ({ activeTab, setActiveTab, postsCount, onFeedClick }) => (
  <div className="bg-white/5 backdrop-blur-xl rounded-2xl border border-purple-500/20 p-6 sticky top-24">
    <div className="space-y-4">
      <button
        onClick={() => { setActiveTab('feed'); onFeedClick(); }}
        className={`w-full text-left px-4 py-3 rounded-xl transition-all ${
          activeTab === 'feed'
            ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white'
            : 'text-gray-300 hover:bg-white/5'
        }`}
      >
        <div className="flex items-center space-x-3">
          <TrendingUp className="w-5 h-5" />
          <span className="font-semibold">Feed</span>
        </div>
      </button>
      <div className="pt-4 border-t border-purple-500/20">
        <h3 className="text-gray-400 text-sm font-semibold mb-3 px-4">Stats</h3>
        <div className="space-y-2 text-gray-300">
          <div className="px-4 py-2">
            <div className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              {postsCount}
            </div>
            <div className="text-sm text-gray-400">Total Posts</div>
          </div>
        </div>
      </div>
    </div>
  </div>
);

export default Sidebar;