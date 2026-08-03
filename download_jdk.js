const https = require('https');
const fs = require('fs');
const path = require('path');

const dest = 'D:/AI/日常工作/jdk17.zip';
const url = 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.13%2B11/OpenJDK17U-jdk_x64_windows_hotspot_17.0.13_11.zip';

function download(url, dest, maxRedirects = 5) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, (res) => {
      // Handle redirects
      if ([301, 302, 303, 307, 308].includes(res.statusCode) && res.headers.location && maxRedirects > 0) {
        console.log('Redirecting to:', res.headers.location);
        res.resume();
        return download(res.headers.location, dest, maxRedirects - 1).then(resolve).catch(reject);
      }

      if (res.statusCode !== 200) {
        res.resume();
        return reject(new Error(`HTTP ${res.statusCode}`));
      }

      const total = parseInt(res.headers['content-length'] || 0);
      let downloaded = 0;
      let lastPct = 0;
      const file = fs.createWriteStream(dest);

      res.on('data', (chunk) => {
        downloaded += chunk.length;
        if (total > 0) {
          const pct = Math.floor(downloaded / total * 100);
          if (pct >= lastPct + 5) {
            lastPct = pct;
            console.log(`${pct}% (${Math.round(downloaded/1024/1024)}MB / ${Math.round(total/1024/1024)}MB)`);
          }
        }
      });

      res.pipe(file);
      file.on('finish', () => {
        file.close();
        const size = fs.statSync(dest).size;
        console.log(`Download complete: ${size} bytes (${Math.round(size/1024/1024)}MB)`);
        resolve(size);
      });
    });

    req.on('error', reject);
    req.setTimeout(300000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
  });
}

console.log('Starting JDK download...');
download(url, dest).then((size) => {
  if (size < 1000000) {
    console.error('ERROR: File too small, download likely failed');
    process.exit(1);
  }
  console.log('SUCCESS');
}).catch((err) => {
  console.error('Download failed:', err.message);
  process.exit(1);
});
