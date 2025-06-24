import React from 'react';
import { motion } from 'framer-motion';

interface WellnessReportProps {
  userStats: any;
  darkMode: boolean;
}

const WellnessReport: React.FC<WellnessReportProps> = ({ darkMode }) => {
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
          <h2 className="text-2xl font-bold mb-4">Digital Wellness Report</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Your personalized wellness insights coming soon!
          </p>
          <div className="text-6xl mb-4">🌱</div>
          <p className="text-sm text-gray-500">
            We're working on comprehensive wellness analytics to help you maintain a healthy digital lifestyle.
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default WellnessReport;
