import { TrendingUp, Users, Smile, Frown } from 'lucide-react';
import { usePosts } from '../contexts/PostContext';

const StatsCard = ({ posts: propPosts }) => {
  const { posts: contextPosts } = usePosts();
  const posts = propPosts || contextPosts;

  // Calculate sentiment statistics
  const positivePosts = posts.filter(p => p.sentiment_label === 'POSITIVE').length;
  const negativePosts = posts.filter(p => p.sentiment_label === 'NEGATIVE').length;
  const postsWithSentiment = posts.filter(p => p.sentiment_label).length;
  const positivePercentage = postsWithSentiment > 0 ? Math.round((positivePosts / postsWithSentiment) * 100) : 0;

  const stats = [
    { icon: TrendingUp, label: 'Total Posts', value: posts.length, gradient: 'from-purple-500 to-pink-500', bgGradient: 'from-purple-500/10 to-pink-500/10' },
    { icon: Users, label: 'Active Users', value: new Set(posts.map(p => p.user)).size, gradient: 'from-blue-500 to-cyan-500', bgGradient: 'from-blue-500/10 to-cyan-500/10' },
    { icon: Smile, label: 'Positive Posts', value: `${positivePercentage}%`, gradient: 'from-green-500 to-emerald-500', bgGradient: 'from-green-500/10 to-emerald-500/10' },
    { icon: Frown, label: 'Negative Posts', value: negativePosts, gradient: 'from-red-500 to-rose-500', bgGradient: 'from-red-500/10 to-rose-500/10' }
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      {stats.map((stat, index) => (
        <div key={index} className={`bg-gradient-to-br ${stat.bgGradient} backdrop-blur-xl rounded-xl border border-purple-500/20 p-4 hover:scale-105 transition-transform cursor-pointer`}>
          <div className={`w-10 h-10 bg-gradient-to-r ${stat.gradient} rounded-lg flex items-center justify-center mb-3`}>
            <stat.icon className="w-5 h-5 text-white" />
          </div>
          <div className={`text-2xl font-bold bg-gradient-to-r ${stat.gradient} bg-clip-text text-transparent`}>{stat.value}</div>
          <div className="text-sm text-gray-400">{stat.label}</div>
        </div>
      ))}
    </div>
  );
};

export default StatsCard;