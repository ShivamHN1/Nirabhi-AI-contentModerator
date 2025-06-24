/**
 * Nirabhi - AI-Powered Content Moderator
 * Main Application Component
 * 
 * This is the heart of our frontend - a beautiful, user-friendly interface
 * that makes content moderation accessible and educational for everyone.
 * 
 * Built with love for creating safer digital spaces! 💙
 */

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Shield, 
  Brain, 
  Heart, 
  Zap, 
  TrendingUp, 
  Users,
  BookOpen,
  Settings
} from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';

// Our custom components
import ContentAnalyzer from './components/ContentAnalyzer';
import Dashboard from './components/Dashboard';
import UserPreferences from './components/UserPreferences';
import WellnessReport from './components/WellnessReport';
import Navigation from './components/Navigation';
import Footer from './components/Footer';

// Types for our application
interface AnalysisResult {
  text: string;
  toxicity_score: number;
  is_toxic: boolean;
  category: string;
  severity: string;
  sentiment_score: number;
  confidence: number;
  explanation: string;
  suggestions: string[];
  support_resources?: Array<{
    name: string;
    description: string;
    contact: string;
    url: string;
  }>;
  analysis_timestamp: string;
  processing_time_ms: number;
}

interface UserStats {
  total_analyses: number;
  toxic_content_rate: number;
  wellness_score: number;
  recent_activity: AnalysisResult[];
}

type ActiveTab = 'analyzer' | 'dashboard' | 'wellness' | 'settings';

function App() {
  // Application state
  const [activeTab, setActiveTab] = useState<ActiveTab>('analyzer');
  const [userStats, setUserStats] = useState<UserStats>({
    total_analyses: 0,
    toxic_content_rate: 0,
    wellness_score: 85,
    recent_activity: []
  });
  const [isLoading, setIsLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  // Load user preferences on startup
  useEffect(() => {
    loadUserPreferences();
    welcomeUser();
  }, []);

  const loadUserPreferences = () => {
    // In a real app, this would load from the backend
    const savedDarkMode = localStorage.getItem('nirabhi_dark_mode');
    if (savedDarkMode) {
      setDarkMode(JSON.parse(savedDarkMode));
    }
  };

  const welcomeUser = () => {
    // Show a friendly welcome message
    toast.success('Welcome to Nirabhi! 🛡️ Let\'s make the internet safer together!', {
      duration: 4000,
      style: {
        background: '#10B981',
        color: '#ffffff',
      },
    });
  };

  const handleAnalysisComplete = (result: AnalysisResult) => {
    // Update user stats with new analysis
    setUserStats(prev => ({
      ...prev,
      total_analyses: prev.total_analyses + 1,
      recent_activity: [result, ...prev.recent_activity.slice(0, 9)] // Keep last 10
    }));

    // Show appropriate feedback based on the result
    if (result.is_toxic) {
      toast.error(`Content flagged as ${result.category}`, {
        icon: '⚠️',
      });
    } else {
      toast.success('Content looks safe! 😊', {
        icon: '✅',
      });
    }
  };

  const toggleDarkMode = () => {
    const newMode = !darkMode;
    setDarkMode(newMode);
    localStorage.setItem('nirabhi_dark_mode', JSON.stringify(newMode));
  };

  // Beautiful animations for tab transitions
  const tabVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -20 }
  };

  const containerClass = `min-h-screen transition-colors duration-300 ${
    darkMode 
      ? 'bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white' 
      : 'bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 text-gray-900'
  }`;

  return (
    <div className={containerClass}>
      {/* Beautiful background pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-600 transform rotate-6 scale-110"></div>
      </div>

      {/* Main content */}
      <div className="relative z-10">
        {/* Header */}
        <header className="pt-8 pb-6">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div 
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center"
            >
              <div className="flex items-center justify-center space-x-3 mb-4">
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                >
                  <Shield className="h-12 w-12 text-blue-500" />
                </motion.div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Nirabhi
                </h1>
              </div>
              <p className="text-lg opacity-80 max-w-2xl mx-auto">
                AI-Powered Content Moderator • Creating Safer Digital Spaces
              </p>
              
              {/* Quick stats */}
              <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 max-w-md mx-auto">
                <motion.div 
                  whileHover={{ scale: 1.05 }}
                  className={`p-3 rounded-lg ${darkMode ? 'bg-gray-800' : 'bg-white'} bg-opacity-50 backdrop-blur-sm`}
                >
                  <div className="flex items-center space-x-2">
                    <Brain className="h-5 w-5 text-blue-500" />
                    <span className="text-sm font-medium">{userStats.total_analyses} Analyzed</span>
                  </div>
                </motion.div>
                
                <motion.div 
                  whileHover={{ scale: 1.05 }}
                  className={`p-3 rounded-lg ${darkMode ? 'bg-gray-800' : 'bg-white'} bg-opacity-50 backdrop-blur-sm`}
                >
                  <div className="flex items-center space-x-2">
                    <Heart className="h-5 w-5 text-pink-500" />
                    <span className="text-sm font-medium">{userStats.wellness_score}% Wellness</span>
                  </div>
                </motion.div>
                
                <motion.div 
                  whileHover={{ scale: 1.05 }}
                  className={`p-3 rounded-lg ${darkMode ? 'bg-gray-800' : 'bg-white'} bg-opacity-50 backdrop-blur-sm`}
                >
                  <div className="flex items-center space-x-2">
                    <Zap className="h-5 w-5 text-yellow-500" />
                    <span className="text-sm font-medium">Real-time</span>
                  </div>
                </motion.div>
              </div>
            </motion.div>
          </div>
        </header>

        {/* Navigation */}
        <Navigation 
          activeTab={activeTab} 
          onTabChange={setActiveTab}
          darkMode={darkMode}
          onDarkModeToggle={toggleDarkMode}
        />

        {/* Main content area */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              variants={tabVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              transition={{ duration: 0.3 }}
            >
              {activeTab === 'analyzer' && (
                <ContentAnalyzer 
                  onAnalysisComplete={handleAnalysisComplete}
                  darkMode={darkMode}
                />
              )}
              
              {activeTab === 'dashboard' && (
                <Dashboard 
                  userStats={userStats}
                  darkMode={darkMode}
                />
              )}
              
              {activeTab === 'wellness' && (
                <WellnessReport 
                  userStats={userStats}
                  darkMode={darkMode}
                />
              )}
              
              {activeTab === 'settings' && (
                <UserPreferences 
                  darkMode={darkMode}
                />
              )}
            </motion.div>
          </AnimatePresence>
        </main>

        {/* Footer */}
        <Footer darkMode={darkMode} />
      </div>

      {/* Toast notifications */}
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: darkMode ? '#374151' : '#ffffff',
            color: darkMode ? '#ffffff' : '#111827',
          },
        }}
      />

      {/* Loading overlay */}
      <AnimatePresence>
        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm z-50 flex items-center justify-center"
          >
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full"
            />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
