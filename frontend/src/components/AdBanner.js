import React, { useState, useEffect } from 'react';
import api from '../utils/api';
import { Card } from './ui/card';
import { Mail, Phone, ExternalLink } from 'lucide-react';

export const AdBanner = () => {
  const [banners, setBanners] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const fetchBanners = async () => {
      try {
        const response = await api.get('/ad-banners');
        setBanners(response.data);
      } catch (error) {
        console.error('Failed to load banners:', error);
      }
    };
    
    fetchBanners();
  }, []);

  useEffect(() => {
    if (banners.length > 0) {
      const interval = setInterval(() => {
        setCurrentIndex((prevIndex) => (prevIndex + 1) % banners.length);
      }, 5000); // Change every 5 seconds
      
      return () => clearInterval(interval);
    }
  }, [banners]);

  if (banners.length === 0) return null;

  const currentBanner = banners[currentIndex];

  return (
    <Card 
      data-testid="ad-banner" 
      className="bg-gradient-to-r from-emerald-50 to-teal-50 border-emerald-200 p-4 mb-6 relative overflow-hidden"
    >
      <div className="flex items-center gap-4">
        {currentBanner.image_url && (
          <img 
            src={currentBanner.image_url} 
            alt={currentBanner.title}
            className="w-20 h-20 object-cover rounded-lg"
            data-testid="ad-banner-image"
          />
        )}
        <div className="flex-1">
          <h3 className="font-semibold text-emerald-900" data-testid="ad-banner-title">{currentBanner.title}</h3>
          <p className="text-sm text-emerald-700" data-testid="ad-banner-text">{currentBanner.text}</p>
          <div className="flex gap-4 mt-2 text-xs text-emerald-600">
            {currentBanner.phone && (
              <span className="flex items-center gap-1" data-testid="ad-banner-phone">
                <Phone className="w-3 h-3" /> {currentBanner.phone}
              </span>
            )}
            {currentBanner.email && (
              <span className="flex items-center gap-1" data-testid="ad-banner-email">
                <Mail className="w-3 h-3" /> {currentBanner.email}
              </span>
            )}
            {currentBanner.link && (
              <a 
                href={currentBanner.link} 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center gap-1 hover:text-emerald-800"
                data-testid="ad-banner-link"
              >
                <ExternalLink className="w-3 h-3" /> Visiter
              </a>
            )}
          </div>
        </div>
      </div>
      <div className="absolute right-4 bottom-4 flex gap-1">
        {banners.map((_, idx) => (
          <div
            key={idx}
            className={`w-2 h-2 rounded-full transition-colors ${
              idx === currentIndex ? 'bg-emerald-600' : 'bg-emerald-200'
            }`}
          />
        ))}
      </div>
    </Card>
  );
};