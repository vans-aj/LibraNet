// Audiobook player JS
(function(){
  'use strict';

  document.addEventListener('DOMContentLoaded', function(){
    const audio = document.getElementById('audio');
    if (!audio) return;

    const playBtn = document.getElementById('playBtn');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const seekBar = document.getElementById('seekBar');
    const currentTimeEl = document.getElementById('currentTime');
    const durationEl = document.getElementById('duration');
    const volume = document.getElementById('volume');
    const speedBtn = document.getElementById('speedBtn');
    const chapterList = document.getElementById('chapters');

    let chapters = [];
    // Build chapters array from DOM
    if (chapterList) {
      chapters = Array.from(chapterList.querySelectorAll('.chapter-item')).map((el, idx) => ({ el, idx, start: parseFloat(el.dataset.start) || 0 }));
    }

    // Update duration when metadata loaded
    audio.addEventListener('loadedmetadata', () => {
      durationEl.textContent = formatTime(audio.duration || 0);
    });

    // Play/pause
    playBtn.addEventListener('click', () => {
      if (audio.paused) {
        audio.play();
        playBtn.classList.add('playing');
      } else {
        audio.pause();
        playBtn.classList.remove('playing');
      }
    });

    // Update seek and time
    audio.addEventListener('timeupdate', () => {
      if (audio.duration) {
        const pct = (audio.currentTime / audio.duration) * 100;
        seekBar.value = pct;
        currentTimeEl.textContent = formatTime(audio.currentTime);
      }

      // Highlight current chapter
      if (chapters.length) {
        let active = 0;
        for (let i=0;i<chapters.length;i++) {
          if (audio.currentTime >= chapters[i].start) active = i;
          else break;
        }
        chapters.forEach((c, i) => c.el.classList.toggle('active', i === active));
      }
    });

    // Seek bar interactions
    seekBar.addEventListener('input', () => {
      if (audio.duration) {
        audio.currentTime = (seekBar.value / 100) * audio.duration;
      }
    });

    // Volume
    if (volume) {
      audio.volume = parseFloat(volume.value);
      volume.addEventListener('input', () => audio.volume = parseFloat(volume.value));
    }

    // Speed button cycle: 0.75,1,1.25,1.5,2
    const speeds = [0.75,1,1.25,1.5,2];
    let spIndex = 1;
    speedBtn.addEventListener('click', () => {
      spIndex = (spIndex + 1) % speeds.length;
      audio.playbackRate = speeds[spIndex];
      speedBtn.textContent = speeds[spIndex] + '×';
    });

    // Chapter click
    chapters.forEach(c => {
      c.el.addEventListener('click', () => {
        audio.currentTime = c.start;
        audio.play();
        playBtn.classList.add('playing');
      });
    });

    // Prev/next: jump to previous/next chapter
    prevBtn.addEventListener('click', () => {
      if (!chapters.length) return;
      const current = chapters.findIndex(c=>c.el.classList.contains('active')) || 0;
      const target = Math.max(0, current-1);
      audio.currentTime = chapters[target].start;
      audio.play();
    });

    nextBtn.addEventListener('click', () => {
      if (!chapters.length) return;
      const current = chapters.findIndex(c=>c.el.classList.contains('active'));
      const target = Math.min(chapters.length-1, current+1);
      audio.currentTime = chapters[target].start;
      audio.play();
    });

    // Helper
    function formatTime(t){
      if (!isFinite(t) || t <= 0) return '0:00';
      const hrs = Math.floor(t/3600);
      const mins = Math.floor((t%3600)/60);
      const secs = Math.floor(t%60);
      if (hrs>0) return `${hrs}:${String(mins).padStart(2,'0')}:${String(secs).padStart(2,'0')}`;
      return `${mins}:${String(secs).padStart(2,'0')}`;
    }

    // Initialize: set duration placeholders if available via dataset
    if (audio.readyState >= 1) {
      durationEl.textContent = formatTime(audio.duration || 0);
    }

  });
})();
