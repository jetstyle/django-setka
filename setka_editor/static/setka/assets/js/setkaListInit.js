var syncBtn = document.createElement('button');
syncBtn.className = 'sync_data';
syncBtn.innerText = 'Sync with setka';
syncBtn.value = '/setka/api/update'
syncBtn.onclick = sendRequestAndExecute('GET', () => {});

var syncBtnLi = document.createElement('li').appendChild(syncBtn).parentNode;
Array.from(document.getElementsByClassName('object-tools')).forEach(x => x.insertBefore(syncBtnLi, x.firstChild));
