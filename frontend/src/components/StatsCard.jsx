import React from 'react';
import { TrendingUp, Users, Heart, MessageCircle } from 'lucide-react';
import { usePosts } from '../contexts/PostContext';

const StatsCard = () => {
  const { posts } = usePosts();

  const stats = [
    { icon: TrendingUp, label: 'Total Posts', value: posts.length, gradient: 'from-purple-500 to-pink-500', bgGradient: 'from-purple-500/10 to-pink-500/10' },
    { icon: Users, label: 'Active Users', value: new Set(posts.map(p => p.user)).size, gradient: 'from-blue-500 to-cyan-500', bgGradient: 'from-blue-500/10 to-cyan-500/10' },
    { icon: Heart, label: 'Total Likes', value: posts.length * 12, gradient: 'from-pink-500 to-rose-500', bgGradient: 'from-pink-500/10 to-rose-500/10' },
    { icon: MessageCircle, label: 'Comments', value: posts.length * 5, gradient: 'from-green-500 to-emerald-500', bgGradient: 'from-green-500/10 to-emerald-500/10' }
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