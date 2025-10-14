document.addEventListener('DOMContentLoaded', () => {
    const output = document.getElementById('output');
    const searchModal = document.getElementById('search-modal');
    const searchInput = document.getElementById('search-input');
    const mobileSearchInput = document.getElementById('mobile-search-input');
    const body = document.body; // Reference to the body element

    let livePapersDB = [];
    let isMobile = false; // Flag to track device type

    // --- Device Detection Logic ---
    function detectDevice() {
        const userAgent = navigator.userAgent || navigator.vendor || window.opera;
        // Basic detection for common mobile OS and devices
        if (/android/i.test(userAgent) || /iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
            isMobile = true;
        }
        // Even if user agent is not mobile, check for touch support and screen size
        if (!isMobile && ('ontouchstart' in window || navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0)) {
            // Consider it mobile if touch is main input and screen is small
            if (window.innerWidth <= 768) { // Assuming 768px is our breakpoint for mobile
                isMobile = true;
            }
        }

        if (isMobile) {
            body.classList.add('is-mobile');
            // Hide desktop search modal and show mobile search bar by default if JS runs first
            searchModal.classList.add('hidden');
            document.getElementById('mobile-search-container').style.display = 'block';
        } else {
            body.classList.add('is-desktop');
            // Hide mobile search bar on desktop by default
            document.getElementById('mobile-search-container').style.display = 'none';
        }
    }

    detectDevice(); // Run detection on load

    // --- Helper Functions (mostly unchanged) ---
    function addLine(text, className = '') {
        const line = document.createElement('div');
        line.innerHTML = text;
        line.className = `line ${className}`;
        output.appendChild(line);
        window.scrollTo(0, document.body.scrollHeight);
    }

    function sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

    async function showProgressBar(text, duration) {
        const line = document.createElement('div');
        line.className = 'line progress-bar-container';
        line.innerHTML = `<span>${text}</span><div class="progress-bar-wrapper"><div class="progress-bar"></div></div>`;
        output.appendChild(line);
        await sleep(duration);
        line.remove();
    }

    async function fetchDeviceInfo() {
        addLine('Device Information:');
        const cores = navigator.hardwareConcurrency || 'N/A';
        addLine(`  - Logical CPU Cores: <span class="highlight">${cores}</span>`);
        const memory = navigator.deviceMemory ? `${navigator.deviceMemory} GB (browser approx.)` : 'N/A';
        addLine(`  - Device Memory (RAM): <span class="highlight">${memory}</span>`);
        if (navigator.storage && navigator.storage.estimate) {
            const estimate = await navigator.storage.estimate();
            const usageMB = (estimate.usage / 1024 / 1024).toFixed(2);
            const quotaMB = (estimate.quota / 1024 / 1024).toFixed(2);
            addLine(`  - Browser Storage Quota: <span class="highlight">${usageMB} MB used / ${quotaMB} MB total</span>`);
        } else {
            addLine('  - Browser Storage: API not supported.');
        }
        addLine('// Note: Browser security prevents access to total disk space or system RAM.', 'comment');
    }

    function handleAdminShortcut() {
        addLine('// Admin access requested.', 'comment');
        const promptLine = document.createElement('div');
        promptLine.className = 'line';
        promptLine.innerHTML = `<span class="purple-prompt">// Please enter your name to proceed: </span>`;
        const nameInput = document.createElement('input');
        nameInput.type = 'text';
        nameInput.className = 'command';
        nameInput.style.background = 'transparent';
        nameInput.style.border = 'none';
        nameInput.style.outline = 'none';
        nameInput.style.width = '200px';
        promptLine.appendChild(nameInput);
        output.appendChild(promptLine);
        nameInput.focus();
        nameInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                const adminName = nameInput.value;
                if (adminName) {
                    addLine(`// Welcome, ${adminName}. Redirecting to admin panel...`, 'comment');
                    setTimeout(() => {
                        window.location.href = '/admin';
                    }, 1500);
                }
            }
        });
    }

    function performSearch(query) {
        if (!query) return;
        if (query.trim().toLowerCase() === 'upload') {
            handleAdminShortcut();
            return;
        }
        addLine(`<span class="prompt">user@archives:~$</span> <span class="command">search --query="${query}"</span>`);
        showProgressBar('Searching database...', 1000).then(() => {
            const lowerQuery = query.toLowerCase();
            const results = livePapersDB.filter(paper => {
                const fullText = `${paper.class} ${paper.subject} ${paper.year} ${paper.original_name} ${paper.exam_type} ${paper.medium}`; // Added medium to search
                return fullText.toLowerCase().includes(lowerQuery);
            });
            if (results.length > 0) {
                addLine(`Found <span class="highlight">${results.length}</span> result(s):`);
                results.forEach(paper => {
                    const title = `${paper.class} ${paper.subject} (Sem ${paper.semester}) - ${paper.year}`;
                    addLine(`  <div class="search-result">[${paper.year}] <a href="${paper.url}" target="_blank">${title}</a></div>`);
                });
            } else {
                addLine('No results found for your query.');
            }
            // Only show Ctrl+K prompt if it's a desktop device
            if (!isMobile) {
                addLine(`<br/>// Press Ctrl + K to search again.`, 'comment');
            }
        });
    }

    async function start() {
        addLine('// Welcome to the Terminal Archives.', 'comment'); await sleep(500);
        await showProgressBar('Connecting to archives...', 1500);
        try {
            const response = await fetch('/api/papers');
            livePapersDB = await response.json();
            addLine(`// Connected. <span class="highlight">${livePapersDB.length}</span> papers found in the database.`);
        } catch (error) {
            addLine('// Connection to archives failed. Please check the server.', 'comment');
            console.error('Fetch error:', error);
        }
        await sleep(500);
        await showProgressBar('Initializing system...', 1000);
        addLine('<span class="prompt">system@archives:~$</span> <span class="command">fetch --device-info</span>');
        await fetchDeviceInfo();
        await sleep(500);
        addLine('<span class="prompt">system@archives:~$</span> <span class="command">ready</span>');
        // Conditionally show search instructions
        if (isMobile) {
            addLine('System ready. Use the search bar below.');
        } else {
            addLine('System ready. Press Ctrl + K to search the database.');
        }
    }

    // --- Event Listeners ---
    // Desktop search (Ctrl+K)
    window.addEventListener('keydown', (e) => {
        if (!isMobile && ((e.ctrlKey || e.metaKey) && e.key === 'k')) {
            e.preventDefault();
            searchModal.classList.remove('hidden');
            searchInput.focus();
            searchInput.value = '';
        }
        if (e.key === 'Escape') {
            if (!searchModal.classList.contains('hidden')) {
                searchModal.classList.add('hidden');
            }
        }
    });
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            searchModal.classList.add('hidden');
            performSearch(searchInput.value);
        }
    });

    // Mobile search (typing in the bottom search bar)
    mobileSearchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            performSearch(mobileSearchInput.value);
            mobileSearchInput.value = ''; // Clear input after search
            mobileSearchInput.blur(); // Hide keyboard
        }
    });

    start();
});
