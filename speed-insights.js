/**
 * Vercel Speed Insights Integration
 * This script loads and initializes Vercel Speed Insights for the site
 */

// Import and inject Speed Insights from CDN
(function() {
  // Create script element to load Speed Insights
  var script = document.createElement('script');
  script.type = 'module';
  script.textContent = `
    import { injectSpeedInsights } from 'https://cdn.jsdelivr.net/npm/@vercel/speed-insights@1/+esm';
    
    // Initialize Speed Insights
    injectSpeedInsights({
      debug: false,
      sampleRate: 1
    });
  `;
  
  // Append to document head
  if (document.head) {
    document.head.appendChild(script);
  } else {
    // If head not ready, wait for DOMContentLoaded
    document.addEventListener('DOMContentLoaded', function() {
      document.head.appendChild(script);
    });
  }
})();
