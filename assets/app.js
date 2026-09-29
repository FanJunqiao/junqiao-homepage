/* Progressive enhancement: publications, links, and citations also work without JS. */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  document.getElementById('year').textContent = new Date().getFullYear();

  const navToggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('nav-links');
  navToggle.hidden = false;
  const closeNav = () => {
    nav.classList.remove('open');
    navToggle.setAttribute('aria-expanded', 'false');
    navToggle.setAttribute('aria-label', 'Open navigation');
  };
  navToggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(open));
    navToggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });
  nav.addEventListener('click', (event) => { if (event.target.closest('a')) closeNav(); });
  document.addEventListener('click', (event) => { if (!event.target.closest('.nav')) closeNav(); });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && nav.classList.contains('open')) {
      closeNav();
      navToggle.focus();
    }
  });

  const list = document.getElementById('publication-list');
  const papers = [...list.querySelectorAll('.publication')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  const search = document.getElementById('publication-search');
  const sort = document.getElementById('publication-sort');
  const count = document.getElementById('publication-count');
  const empty = document.getElementById('empty-state');
  const more = document.getElementById('publication-more');
  const pageSize = 5;
  let expanded = false;
  let category = 'all';
  document.querySelector('.publication-tools').hidden = false;
  document.querySelector('.publication-actions').hidden = false;

  const videos = [...document.querySelectorAll('video[data-src]')];
  const motionButton = document.getElementById('motion-toggle');
  const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
  let paused = motionPreference.matches || Boolean(navigator.connection?.saveData);
  let manuallySetMotion = false;
  const inView = new Set();
  const updateMotionLabel = () => {
    motionButton.textContent = paused ? 'Play previews' : 'Pause previews';
    motionButton.setAttribute('aria-pressed', String(paused));
  };
  const syncVideo = (video) => {
    if (paused || document.hidden || video.closest('.publication').hidden || !inView.has(video)) {
      video.pause();
      return;
    }
    if (video.dataset.failed) return;
    if (!video.getAttribute('src')) {
      video.muted = true;
      video.src = video.dataset.src;
    }
    video.play().catch(() => { /* Poster remains available when autoplay is blocked. */ });
  };
  const syncVideos = () => videos.forEach(syncVideo);
  videos.forEach((video) => {
    video.addEventListener('loadeddata', () => video.classList.add('has-frame'));
    video.addEventListener('error', () => {
      video.classList.remove('has-frame');
      video.dataset.failed = 'true';
    });
  });
  if ('IntersectionObserver' in window) {
    const videoObserver = new IntersectionObserver((entries) => {
      entries.forEach(({target, isIntersecting}) => {
        if (isIntersecting) inView.add(target); else inView.delete(target);
        syncVideo(target);
      });
    }, {threshold: 0.1});
    videos.forEach((video) => videoObserver.observe(video));
  } else {
    videos.forEach((video) => inView.add(video));
  }
  motionButton.addEventListener('click', () => {
    manuallySetMotion = true;
    paused = !paused;
    updateMotionLabel();
    syncVideos();
  });
  motionPreference.addEventListener('change', (event) => {
    if (manuallySetMotion) return;
    paused = event.matches || Boolean(navigator.connection?.saveData);
    updateMotionLabel();
    syncVideos();
  });
  document.addEventListener('visibilitychange', syncVideos);
  updateMotionLabel();

  function filterPapers() {
    const terms = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    const ordered = [...list.querySelectorAll('.publication')];
    const matches = ordered.filter((paper) => {
      const matchesCategory = category === 'all' || paper.dataset.categories.split(' ').includes(category);
      const matchesSearch = terms.every((term) => paper.dataset.search.includes(term));
      return matchesCategory && matchesSearch;
    });
    const visible = expanded ? matches : matches.slice(0, pageSize);
    papers.forEach((paper) => { paper.hidden = !visible.includes(paper); });
    filters.forEach((button) => {
      const active = button.dataset.filter === category;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    count.textContent = `Showing ${visible.length} of ${matches.length} publications`;
    empty.hidden = matches.length !== 0;
    more.hidden = matches.length <= pageSize;
    more.textContent = expanded ? 'Show fewer' : `Show all ${matches.length} publications`;
    more.setAttribute('aria-expanded', String(expanded));
    syncVideos();
  }
  document.querySelectorAll('[data-count]').forEach((counter) => {
    const key = counter.dataset.count;
    counter.textContent = papers.filter((paper) => key === 'all' || paper.dataset.categories.split(' ').includes(key)).length;
  });
  filters.forEach((button) => button.addEventListener('click', () => {
    category = button.dataset.filter;
    expanded = false;
    filterPapers();
  }));
  search.addEventListener('input', () => { expanded = false; filterPapers(); });
  sort.addEventListener('change', () => {
    const ordered = [...papers];
    if (sort.value !== 'selected') {
      const direction = sort.value === 'oldest' ? 1 : -1;
      ordered.sort((a, b) => direction * (Number(a.dataset.year) - Number(b.dataset.year)));
    }
    ordered.forEach((paper) => list.append(paper));
    expanded = false;
    filterPapers();
  });
  more.addEventListener('click', () => {
    expanded = !expanded;
    filterPapers();
    if (!expanded) document.getElementById('publications').scrollIntoView({block: 'start'});
  });
  const reset = () => {
    category = 'all';
    search.value = '';
    expanded = false;
    filterPapers();
  };
  document.getElementById('reset-filters').addEventListener('click', () => {
    reset();
    filters[0].focus();
  });
  // A news/award deep link always reveals its publication, even after filtering.
  function revealPaper(hash) {
    const paper = papers.find((item) => '#' + item.id === hash);
    if (!paper) return;
    if (paper.hidden) {
      category = 'all';
      search.value = '';
      expanded = true;
      filterPapers();
    }
    requestAnimationFrame(() => paper.scrollIntoView({block: 'start'}));
  }
  document.addEventListener('click', (event) => {
    const anchor = event.target.closest('a[href^="#"]');
    if (anchor) revealPaper(anchor.getAttribute('href'));
  });
  window.addEventListener('hashchange', () => revealPaper(location.hash));
  filterPapers();
  if (location.hash) revealPaper(location.hash);

  const citationDialog = document.getElementById('citation-dialog');
  const citationCode = document.getElementById('citation-code');
  const copyStatus = document.getElementById('copy-status');
  const copyButton = document.getElementById('copy-citation');
  // Keep the real .bib download link as fallback if <dialog> is unsupported.
  document.querySelectorAll('[data-cite]').forEach((link) => link.addEventListener('click', (event) => {
    if (!citationDialog.showModal) return;
    event.preventDefault();
    const paper = link.closest('.publication');
    document.getElementById('citation-title').textContent = paper.querySelector('h3').textContent;
    citationCode.textContent = paper.querySelector('.bibtex').content.textContent.trim();
    document.getElementById('download-citation').href = link.href;
    copyStatus.textContent = '';
    copyButton.textContent = 'Copy BibTeX';
    citationDialog.showModal();
  }));
  copyButton.addEventListener('click', async () => {
    let copied = false;
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(citationCode.textContent);
        copied = true;
      }
    } catch { /* Fall back to selection on file:// or restrictive browsers. */ }
    if (!copied) {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(citationCode);
      selection.removeAllRanges();
      selection.addRange(range);
      try { copied = document.execCommand('copy'); } catch { /* Manual copy remains available. */ }
      if (copied) selection.removeAllRanges();
    }
    copyButton.textContent = copied ? 'Copied ✓' : 'Copy BibTeX';
    copyStatus.textContent = copied ? 'Citation copied.' : 'Text selected. Press Ctrl+C / ⌘C to copy.';
  });
  const wechat = document.getElementById('wechat-dialog');
  document.getElementById('wechat-link').addEventListener('click', (event) => {
    if (!wechat.showModal) return;
    event.preventDefault();
    document.getElementById('wechat-link').setAttribute('aria-expanded', 'true');
    wechat.showModal();
  });
  if (wechat.showModal) {
    const wechatLink = document.getElementById('wechat-link');
    wechatLink.setAttribute('aria-haspopup', 'dialog');
    wechatLink.setAttribute('aria-controls', 'wechat-dialog');
    wechatLink.setAttribute('aria-expanded', 'false');
    wechat.addEventListener('close', () => wechatLink.setAttribute('aria-expanded', 'false'));
  }
  document.querySelectorAll('dialog').forEach((dialog) => {
    dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', (event) => {
      const box = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) dialog.close();
    });
  });

  const navLinks = [...nav.querySelectorAll('a[href^="#"]')];
  let scrollPending = false;
  function updateNav() {
    let active = navLinks[0];
    navLinks.forEach((link) => {
      if (document.querySelector(link.getAttribute('href')).getBoundingClientRect().top <= 150) active = link;
    });
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 10) active = navLinks.at(-1);
    navLinks.forEach((link) => {
      link.classList.toggle('active', link === active);
      if (link === active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
    });
    scrollPending = false;
  }
  window.addEventListener('scroll', () => {
    if (!scrollPending) { scrollPending = true; requestAnimationFrame(updateNav); }
  }, {passive: true});
  updateNav();
})();
