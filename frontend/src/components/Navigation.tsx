/**
 * Navigation Component
 * 
 * Beautiful, responsive navigation that allows users to switch between
 * different sections of the application with smooth animations.
 */

import React from 'react';
import { motion } from 'framer-motion';
import { 
  Search, 
  BarChart3, 
  Heart, 
  Settings, 
  Moon, 
  Sun 
} from 'lucide-react';

type ActiveTab = 'analyzer' | 'dashboard' | 'wellness' | 'settings';

interface NavigationProps {
  activeTab: ActiveTab;
  onTabChange: (tab: ActiveTab) => void;
  darkMode: boolean;
  onDarkModeToggle: () => void;
}

const Navigation: React.FC<NavigationProps> = ({
  activeTab,
  onTabChange,
  darkMode,
  onDarkModeToggle
}) => {
  const navItems = [
    {
      id: 'analyzer' as ActiveTab,
      label: 'Analyzer',
      icon: Search,
      description: 'Analyze content for toxicity'
    },
    {
      id: 'dashboard' as ActiveTab,
      label: 'Dashboard',
      icon: BarChart3,
      description: 'View analytics and trends'
    },
    {
      id: 'wellness' as ActiveTab,
      label: 'Wellness',
      icon: Heart,
      description: 'Digital wellness insights'
    },
    {
      id: 'settings' as ActiveTab,
      label: 'Settings',
      icon: Settings,
      description: 'Customize preferences'
    }
  ];

  const navClass = `relative mx-auto max-w-2xl rounded-full p-1 shadow-lg backdrop-blur-sm transition-all duration-300 ${
    darkMode 
      ? 'bg-gray-800 bg-opacity-50 border border-gray-700' 
      : 'bg-white bg-opacity-70 border border-gray-200'
  }`;

  return (
    <nav className="sticky top-4 z-40 px-4">
      <div className={navClass}>
        <div className="flex items-center justify-between">
          {/* Navigation Items */}
          <div className="flex items-center space-x-1">
            {navItems.map((item) => {
              const isActive = activeTab === item.id;
              const Icon = item.icon;
              
              return (
                <motion.button
                  key={item.id}
                  onClick={() => onTabChange(item.id)}
                  className={`relative flex items-center space-x-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                    isActive
                      ? darkMode
                        ? 'text-white'
                        : 'text-gray-900'
                      : darkMode
                        ? 'text-gray-400 hover:text-white'
                        : 'text-gray-600 hover:text-gray-900'
                  }`}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {/* Active background */}
                  {isActive && (
                    <motion.div
                      layoutId="activeTab"
                      className={`absolute inset-0 rounded-full ${
                        darkMode
                          ? 'bg-gradient-to-r from-blue-600 to-purple-600'
                          : 'bg-gradient-to-r from-blue-500 to-purple-500'
                      } shadow-lg`}
                      transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                    />
                  )}
                  
                  {/* Icon and label */}
                  <div className="relative flex items-center space-x-2">
                    <Icon className="h-4 w-4" />
                    <span className="hidden sm:inline">{item.label}</span>
                  </div>
                </motion.button>
              );
            })}
          </div>

          {/* Dark mode toggle */}
          <motion.button
            onClick={onDarkModeToggle}
            className={`p-2 rounded-full transition-all duration-200 ${
              darkMode
                ? 'text-yellow-400 hover:bg-gray-700'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            title={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            <motion.div
              initial={false}
              animate={{ rotate: darkMode ? 180 : 0 }}
              transition={{ duration: 0.3 }}
            >
              {darkMode ? (
                <Sun className="h-4 w-4" />
              ) : (
                <Moon className="h-4 w-4" />
              )}
            </motion.div>
          </motion.button>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
