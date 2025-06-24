/**
 * Dashboard Component
 * 
 * Provides users with analytics, trends, and insights about their
 * digital environment and content analysis history.
 */

import React from 'react';
import { motion } from 'framer-motion';
import { 
  TrendingUp, 
  Shield, 
  BarChart3, 
  Activity,
  Clock,
  ThumbsUp
} from 'lucide-react';

interface UserStats {
  total_analyses: number;
  toxic_content_rate: number;
  wellness_score: number;
  recent_activity: any[];
}

interface DashboardProps {
  userStats: UserStats;
  darkMode: boolean;
}

const Dashboard: React.FC<DashboardProps> = ({ userStats, darkMode }) => {
  const cardClass = `rounded-xl shadow-lg backdrop-blur-sm transition-all duration-300 ${
    darkMode 
      ? 'bg-gray-800 bg-opacity-50 border border-gray-700' 
      : 'bg-white bg-opacity-70 border border-gray-200'
  }`;

  const stats = [
    {
      label: 'Total Analyses',
      value: userStats.total_analyses,
      icon: BarChart3,
      color: 'blue',
      change: '+12%'
    },
    {
      label: 'Wellness Score',
      value: `${userStats.wellness_score}%`,
      icon: Shield,
      color: 'green',
      change: '+5%'
    },
    {
      label: 'Safe Content',
      value: `${(100 - userStats.toxic_content_rate).toFixed(1)}%`,
      icon: ThumbsUp,
      color: 'purple',
      change: '+2%'
    }
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h2 className="text-2xl font-bold mb-2">Your Digital Wellness Dashboard</h2>
        <p className="text-gray-600 dark:text-gray-400">
          Track your progress in creating a safer digital environment
        </p>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className={cardClass}
            >
              <div className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">{stat.label}</p>
                    <p className="text-2xl font-bold">{stat.value}</p>
                    <p className={`text-sm text-${stat.color}-500`}>{stat.change} this week</p>
                  </div>
                  <div className={`p-3 rounded-full bg-${stat.color}-100 dark:bg-${stat.color}-900`}>
                    <Icon className={`h-6 w-6 text-${stat.color}-500`} />
                  </div>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Recent Activity */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className={cardClass}
      >
        <div className="p-6">
          <div className="flex items-center space-x-3 mb-4">
            <Activity className="h-6 w-6 text-blue-500" />
            <h3 className="text-lg font-semibold">Recent Activity</h3>
          </div>
          
          {userStats.recent_activity.length > 0 ? (
            <div className="space-y-3">
              {userStats.recent_activity.slice(0, 5).map((activity, index) => (
                <div key={index} className={`p-3 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-50'}`}>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium">
                        {activity.category === 'safe' ? '✅ Safe content' : '⚠️ Flagged content'}
                      </p>
                      <p className="text-xs text-gray-500 truncate max-w-md">
                        "{activity.text.substring(0, 50)}..."
                      </p>
                    </div>
                    <div className="flex items-center space-x-2 text-xs text-gray-500">
                      <Clock className="h-3 w-3" />
                      <span>Just now</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <TrendingUp className="h-12 w-12 text-gray-400 mx-auto mb-3" />
              <p className="text-gray-500">No activity yet. Start analyzing content to see your stats!</p>
            </div>
          )}
        </div>
      </motion.div>

      {/* Tips */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className={cardClass}
      >
        <div className="p-6">
          <h3 className="text-lg font-semibold mb-4">💡 Tips for Digital Wellness</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-blue-50'}`}>
              <h4 className="font-medium mb-2">Take Regular Breaks</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Step away from screens every hour to maintain mental clarity.
              </p>
            </div>
            <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-green-50'}`}>
              <h4 className="font-medium mb-2">Curate Your Feed</h4>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Follow accounts that promote positivity and learning.
              </p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;
