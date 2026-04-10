// Initialize Lucide Icons
if (window.lucide) {
  window.lucide.createIcons();
}

// Scripture Data
const scriptures = [
  { text: '"The Lord is my shepherd; I shall not want."', ref: "Psalm 23:1" },
  { text: '"But they that wait upon the Lord shall renew their strength; they shall mount up with wings as eagles."', ref: "Isaiah 40:31" },
  { text: '"I can do all things through Christ which strengtheneth me."', ref: "Philippians 4:13" },
  { text: '"Trust in the Lord with all thine heart; and lean not unto thine own understanding."', ref: "Proverbs 3:5" },
  { text: '"For I know the thoughts that I think toward you, saith the Lord, thoughts of peace, and not of evil."', ref: "Jeremiah 29:11" }
];

let currentScriptureIndex = 0;
const verseTextEl = document.getElementById('verse-text');
const verseRefEl = document.getElementById('verse-ref');
const dots = document.querySelectorAll('.dot');

function updateScripture(index) {
  // Fade out
  verseTextEl.style.opacity = '0';
  verseRefEl.style.opacity = '0';
  
  setTimeout(() => {
    const scripture = scriptures[index];
    verseTextEl.textContent = scripture.text;
    verseRefEl.textContent = scripture.ref;
    
    // Update dots
    dots.forEach((dot, i) => {
      dot.classList.toggle('active', i === index);
    });
    
    // Fade in
    verseTextEl.style.opacity = '1';
    verseRefEl.style.opacity = '1';
    verseTextEl.style.transition = 'opacity 0.5s ease-in-out';
    verseRefEl.style.transition = 'opacity 0.5s ease-in-out';
  }, 500);
}

// Auto Rotate Scripture
setInterval(() => {
  currentScriptureIndex = (currentScriptureIndex + 1) % scriptures.length;
  updateScripture(currentScriptureIndex);
}, 8000);

// Dot Navigation
dots.forEach((dot, index) => {
  dot.addEventListener('click', () => {
    currentScriptureIndex = index;
    updateScripture(currentScriptureIndex);
  });
});

// Mobile Menu
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileOverlay = document.getElementById('mobile-overlay');
const mobileLinks = document.querySelectorAll('.mobile-links a');

if (mobileMenuBtn && mobileOverlay) {
  mobileMenuBtn.addEventListener('click', () => {
    mobileOverlay.classList.toggle('active');
    const icon = mobileOverlay.classList.contains('active') ? 'x' : 'menu';
    mobileMenuBtn.innerHTML = `<i data-lucide="${icon}"></i>`;
    window.lucide.createIcons();
  });

  mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
      mobileOverlay.classList.remove('active');
      mobileMenuBtn.innerHTML = `<i data-lucide="menu"></i>`;
      window.lucide.createIcons();
    });
  });
}

// Scroll Animations
const observerOptions = {
  threshold: 0.15,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      // Optional: stop observing after animation
      // observer.unobserve(entry.target);
    }
  });
}, observerOptions);

document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right').forEach(el => {
  observer.observe(el);
});

// Sticky Navbar Background
window.addEventListener('scroll', () => {
  const navbar = document.getElementById('navbar');
  if (window.scrollY > 50) {
    navbar.style.background = 'rgba(255, 255, 255, 0.98)';
    navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
  } else {
    navbar.style.background = 'rgba(255, 255, 255, 0.95)';
    navbar.style.boxShadow = 'none';
  }
});

// Form Handling
const handleFormSubmit = (formId, successMessage) => {
  const form = document.getElementById(formId);
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalBtnText = submitBtn.textContent;
      
      submitBtn.textContent = 'Sending...';
      submitBtn.disabled = true;
      
      // Simulate API call
      setTimeout(() => {
        alert(successMessage);
        form.reset();
        submitBtn.textContent = originalBtnText;
        submitBtn.disabled = false;
      }, 1500);
    });
  }
};

handleFormSubmit('prayer-form', 'Thank you for sharing your prayer request. We will be praying for you!');
handleFormSubmit('testimony-form', 'Thank you for sharing your story of God\'s grace! Your testimony will be reviewed.');

// Admin Button (redirect to full admin console)
const adminBtn = document.querySelector('.admin-btn');
if (adminBtn) {
  adminBtn.addEventListener('click', () => {
    window.open('/admin.html', '_blank', 'noopener');
  });
}
