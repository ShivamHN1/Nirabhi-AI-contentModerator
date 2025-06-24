import React from 'react';
import { Heart, Github, Twitter, Mail } from 'lucide-react';

interface FooterProps {
  darkMode: boolean;
}

const Footer: React.FC<FooterProps> = ({ darkMode }) => {
  return (
    <footer className="mt-16 py-8 border-t border-gray-200 dark:border-gray-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <div className="flex items-center justify-center space-x-1 mb-4">
            <span className="text-sm text-gray-600 dark:text-gray-400">
              Built with
            </span>
            <Heart className="h-4 w-4 text-red-500" />
            <span className="text-sm text-gray-600 dark:text-gray-400">
              for creating safer digital spaces
            </span>
          </div>
          
          <p className="text-xs text-gray-500 mb-4">
            © 2024 Nirabhi AI Content Moderator. Empowering digital wellness through technology.
          </p>
          
          <div className="flex justify-center space-x-4">
            <a href="#" className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
              <Github className="h-5 w-5" />
            </a>
            <a href="#" className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
              <Twitter className="h-5 w-5" />
            </a>
            <a href="#" className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
              <Mail className="h-5 w-5" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
