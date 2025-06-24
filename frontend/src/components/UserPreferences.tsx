import React from 'react';
import { motion } from 'framer-motion';

interface UserPreferencesProps {
  darkMode: boolean;
}

const UserPreferences: React.FC<UserPreferencesProps> = ({ darkMode }) => {
  const cardClass = `rounded-xl shadow-lg backdrop-blur-sm transition-all duration-300 ${
    darkMode 
      ? 'bg-gray-800 bg-opacity-50 border border-gray-700' 
      : 'bg-white bg-opacity-70 border border-gray-200'
  }`;

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className={cardClass}
      >
        <div className="p-8 text-center">
          <h2 className="text-2xl font-bold mb-4">User Preferences</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Customize your content moderation experience
          </p>
          <div className="text-6xl mb-4">⚙️</div>
          <p className="text-sm text-gray-500">
            Advanced preference settings will be available soon to personalize your moderation experience.
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default UserPreferences;
