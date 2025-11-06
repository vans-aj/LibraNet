// Enhanced Audiobook Player with Chapter Support
(function(){
  'use strict';

  document.addEventListener('DOMContentLoaded', function(){
    console.log('=== Audiobook Player Initializing ===');
    
    const audio = document.getElementById('audio');
    if (!audio) {
      console.error('Audio element not found!');
      return;
    }
    console.log('✓ Audio element found');

    // Get chapters data from template
    const chapters = window.chaptersData || [];
    console.log(`Chapters data:`, chapters);
    
    if (!chapters.length) {
      console.error('❌ No chapters found!');
      return;
    }
    console.log(`✓ Found ${chapters.length} chapters`)

    // UI Elements
    const playBtn = document.getElementById('playBtn');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const rewindBtn = document.getElementById('rewindBtn');
    const forwardBtn = document.getElementById('forwardBtn');
    const seekBar = document.getElementById('seekBar');
    const currentTimeEl = document.getElementById('currentTime');
    const durationEl = document.getElementById('duration');
    const volume = document.getElementById('volume');
    const chapterTitle = document.getElementById('chapterTitle');
    const currentChapterNum = document.getElementById('currentChapterNum');
    const chapterItems = document.querySelectorAll('.chapter-item');
    const playIcon = document.getElementById('playIcon');
    const pauseIcon = document.getElementById('pauseIcon');

    // Player state
    let currentChapterIndex = 0;
    let isPlaying = false;

    // Load a chapter
    function loadChapter(index) {
      console.log(`📀 loadChapter called with index: ${index}`);
      
      if (index < 0 || index >= chapters.length) {
        console.error(`❌ Invalid chapter index: ${index}`);
        return;
      }
      
      currentChapterIndex = index;
      const chapter = chapters[index];
      
      console.log(`📖 Loading chapter:`, chapter);
      
      // Update audio source
      audio.src = chapter.url;
      console.log(`🔗 Audio src set to: ${audio.src}`);
      
      audio.load();
      console.log('⏳ Audio.load() called');
      
      // Update UI
      chapterTitle.textContent = chapter.title;
      currentChapterNum.textContent = chapter.number;
      
      // Update chapter list highlighting
      chapterItems.forEach((item, i) => {
        item.classList.toggle('active', i === index);
      });
      
      // Update button states
      prevBtn.disabled = (index === 0);
      nextBtn.disabled = (index === chapters.length - 1);
      
      console.log(`✅ Chapter ${chapter.number}: ${chapter.title} loaded`);
    }

    // Play/Pause
    function togglePlay() {
      console.log('togglePlay called, audio.paused:', audio.paused);
      console.log('audio.src:', audio.src);
      console.log('audio.readyState:', audio.readyState);
      
      if (audio.paused) {
        console.log('Attempting to play...');
        audio.play().then(() => {
          console.log('✓ Play successful');
          isPlaying = true;
          updatePlayButton();
        }).catch(err => {
          console.error('❌ Play failed:', err);
          console.error('Error name:', err.name);
          console.error('Error message:', err.message);
          alert('Failed to play audio: ' + err.message);
        });
      } else {
        console.log('Pausing audio...');
        audio.pause();
        isPlaying = false;
        updatePlayButton();
      }
    }

    function updatePlayButton() {
      console.log('updatePlayButton called, isPlaying:', isPlaying);
      if (isPlaying) {
        playIcon.style.display = 'none';
        pauseIcon.style.display = 'block';
        playBtn.classList.add('playing');
      } else {
        playIcon.style.display = 'block';
        pauseIcon.style.display = 'none';
        playBtn.classList.remove('playing');
      }
    }

    // Event Listeners
    playBtn.addEventListener('click', togglePlay);

    prevBtn.addEventListener('click', () => {
      if (currentChapterIndex > 0) {
        loadChapter(currentChapterIndex - 1);
        if (isPlaying) audio.play();
      }
    });

    nextBtn.addEventListener('click', () => {
      if (currentChapterIndex < chapters.length - 1) {
        loadChapter(currentChapterIndex + 1);
        if (isPlaying) audio.play();
      }
    });

    rewindBtn.addEventListener('click', () => {
      audio.currentTime = Math.max(0, audio.currentTime - 10);
    });

    forwardBtn.addEventListener('click', () => {
      audio.currentTime = Math.min(audio.duration, audio.currentTime + 30);
    });

    // Volume control
    if (volume) {
      audio.volume = parseFloat(volume.value);
      volume.addEventListener('input', () => {
        audio.volume = parseFloat(volume.value);
        updateVolumeIcon();
      });
    }

    function updateVolumeIcon() {
      const wave1 = document.getElementById('volumeWave1');
      const wave2 = document.getElementById('volumeWave2');
      if (audio.volume === 0) {
        wave1.style.display = 'none';
        wave2.style.display = 'none';
      } else if (audio.volume < 0.5) {
        wave1.style.display = 'block';
        wave2.style.display = 'none';
      } else {
        wave1.style.display = 'block';
        wave2.style.display = 'block';
      }
    }

    // Seek bar
    seekBar.addEventListener('input', () => {
      if (audio.duration) {
        audio.currentTime = (seekBar.value / 100) * audio.duration;
      }
    });

    // Time update
    audio.addEventListener('timeupdate', () => {
      if (audio.duration) {
        const pct = (audio.currentTime / audio.duration) * 100;
        seekBar.value = pct;
        currentTimeEl.textContent = formatTime(audio.currentTime);
      }
    });

    // Metadata loaded
    audio.addEventListener('loadedmetadata', () => {
      console.log('✓ Audio metadata loaded');
      durationEl.textContent = formatTime(audio.duration || 0);
      seekBar.max = 100;
    });
    
    // Error handling
    audio.addEventListener('error', (e) => {
      console.error('Audio error:', e);
      console.error('Audio error code:', audio.error ? audio.error.code : 'unknown');
      console.error('Audio error message:', audio.error ? audio.error.message : 'unknown');
      
      // Try to skip to next chapter if available
      if (currentChapterIndex < chapters.length - 1) {
        console.log('Trying next chapter...');
        loadChapter(currentChapterIndex + 1);
      } else {
        chapterTitle.textContent = 'Error loading audio';
      }
    });
    
    // Can play through
    audio.addEventListener('canplaythrough', () => {
      console.log('✓ Audio ready to play');
    });

    // Auto-play next chapter when current ends
    audio.addEventListener('ended', () => {
      if (currentChapterIndex < chapters.length - 1) {
        loadChapter(currentChapterIndex + 1);
        audio.play();
      } else {
        isPlaying = false;
        updatePlayButton();
      }
    });

    // Audio state changes
    audio.addEventListener('play', () => {
      isPlaying = true;
      updatePlayButton();
    });

    audio.addEventListener('pause', () => {
      isPlaying = false;
      updatePlayButton();
    });

    // Chapter list clicks
    chapterItems.forEach((item, index) => {
      item.addEventListener('click', () => {
        loadChapter(index);
        if (isPlaying) {
          audio.play();
        }
      });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT') return; // Don't trigger when typing
      
      switch(e.key) {
        case ' ':
          e.preventDefault();
          togglePlay();
          break;
        case 'ArrowLeft':
          e.preventDefault();
          audio.currentTime = Math.max(0, audio.currentTime - 5);
          break;
        case 'ArrowRight':
          e.preventDefault();
          audio.currentTime = Math.min(audio.duration, audio.currentTime + 5);
          break;
        case 'ArrowUp':
          e.preventDefault();
          audio.volume = Math.min(1, audio.volume + 0.1);
          volume.value = audio.volume;
          updateVolumeIcon();
          break;
        case 'ArrowDown':
          e.preventDefault();
          audio.volume = Math.max(0, audio.volume - 0.1);
          volume.value = audio.volume;
          updateVolumeIcon();
          break;
      }
    });

    // Format time helper
    function formatTime(seconds) {
      if (!isFinite(seconds) || seconds <= 0) return '0:00';
      
      const hrs = Math.floor(seconds / 3600);
      const mins = Math.floor((seconds % 3600) / 60);
      const secs = Math.floor(seconds % 60);
      
      if (hrs > 0) {
        return `${hrs}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      }
      return `${mins}:${String(secs).padStart(2, '0')}`;
    }

    // Initialize player
    loadChapter(0);
    updateVolumeIcon();
    updatePlayButton();
    
    console.log(`Audiobook player initialized with ${chapters.length} chapters`);
  });
})();
