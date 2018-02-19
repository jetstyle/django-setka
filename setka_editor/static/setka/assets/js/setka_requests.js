var sendRequestAndReload = type_ => sendRequestAndExecute(type_, () => location.reload());
Array.from(document.getElementsByClassName('setkapost')).forEach(elem => elem.onclick = sendRequestAndReload('POST'));
Array.from(document.getElementsByClassName('setkadelete')).forEach(elem => elem.onclick = sendRequestAndReload('DELETE'));

function sendRequestAndExecute(type_, func) {
    return function () {
        var xhr = new XMLHttpRequest();
        xhr.open(type_, this.value, true);
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        xhr.send();
        xhr.onreadystatechange = function() {
            if (xhr.readyState != 4) return;
            if (xhr.status === 200) func();
        }
    }
}

function getCookie(name) {
    if (document.cookie && document.cookie !== '') {
        return document.cookie.split(';').filter(x => x.indexOf('csrftoken') !== -1).map(x => x.split('=')[1])[0];
    }
    return '';
}
