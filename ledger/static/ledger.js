(function(){
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');
    let files = [];

    if (!dropzone || !fileInput || !fileList) {
        console.warn('Ledger upload assets missing in template.');
        return;
    }

    dropzone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        addFiles(Array.from(e.target.files));
        fileInput.value = '';
    });

    ['dragenter','dragover'].forEach(ev => {
        dropzone.addEventListener(ev, (e) => {
            e.preventDefault();
            dropzone.classList.add('drag');
        });
    });

    ['dragleave','drop'].forEach(ev => {
        dropzone.addEventListener(ev, (e) => {
            e.preventDefault();
            dropzone.classList.remove('drag');
        });
    });

    dropzone.addEventListener('drop', (e) => {
        const dropped = Array.from(e.dataTransfer.files);
        addFiles(dropped);
    });

    function addFiles(newFiles){
        newFiles.forEach(f => {
            files.push(f);
        });
        renderFiles();
    }

    function renderFiles(){
        fileList.innerHTML = '';
        files.forEach((f, idx) => {
            const el = document.createElement('div');
            el.className = 'file-row';
            const nameSpan = document.createElement('span');
            nameSpan.textContent = `${f.name} (${Math.round(f.size/1024)} KB)`;
            el.appendChild(nameSpan);
            
            const btn = document.createElement('button');
            btn.textContent = 'Remove';
            btn.addEventListener('click', (ev) => {
                ev.preventDefault();
                files.splice(idx,1);
                renderFiles();
            });
            el.appendChild(btn);
            fileList.appendChild(el);
        });
    }

    document.getElementById('metaForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const resource_id = document.getElementById('resource_id').value;
        const created_by = document.getElementById('created_by').value;
        const metadata = document.getElementById('metadata').value;

        if (!resource_id) {
            alert('resource_id is required');
            return;
        }

        const form = new FormData();
        form.append('resource_id', resource_id);
        if (created_by) form.append('created_by', created_by);
        if (metadata) form.append('metadata', metadata);
        files.forEach((f, i) => form.append('file' + i, f));

        const respEl = document.getElementById('response');
        respEl.textContent = 'Uploading...';

        try{
            const res = await fetch('/ledger/metadata', {
                method: 'POST',
                body: form
            });
            const json = await res.json();
            respEl.textContent = JSON.stringify(json, null, 2);
            
            if (json && json.ok) {
                files = [];
                renderFiles();
                document.getElementById('metadata').value = '{}';
            }
        }catch(err){
            respEl.textContent = 'Upload error: ' + err.message;
        }
    });
})();
