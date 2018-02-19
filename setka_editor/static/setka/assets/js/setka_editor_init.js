var hideElements = elems => Array.from(elems).forEach(elem => elem.style.display = 'none');
hideElements(document.getElementsByClassName('field-setla_layout_id'));
hideElements(document.getElementsByClassName('field-setka_theme_id'));

var stkEditor = document.createElement('div');
stkEditor.className = 'stk-editor';
stkEditor.id = 'setka-editor';

var field_content = Array.from(document.getElementsByClassName('field-content'));
field_content.forEach(x => hideElements(x.getElementsByTagName('div')));
field_content[0].appendChild(stkEditor);

var conf = {exists: false}
var content = document.getElementById('id_content');
if ('value' in content && content.value.length > 0) {
    conf.postContent = content.value;
    conf.postThemeID = document.getElementById('id_setka_theme_id').value;
    conf.postLayoutID = document.getElementById('id_setla_layout_id').value;
    conf.exists = true;
}

conf.images = getAllImages();
if (!conf.images.error) {
    fetch(theme_json).then(response => response.json()).then(response => {
        const config = response.config;
        const assets = response.assets;
        config.public_token = setka_public_token

        if (conf.exists) {
            config.theme = conf.postThemeID;
            config.layout = conf.postLayoutID;
        }

        config.restApiUrl = '/setka/api/';
        if (conf.images.data.length > 0) assets.images = conf.images.data;

        SetkaEditor.start(config, assets);
        if (conf.exists) SetkaEditor.replaceHTML(conf.postContent);
    }).catch(ex => alert(ex));
}

Array.from(document.getElementById('content-main').children).filter(x => x.tagName == 'FORM').map(x => x.onclick = function() {
    document.getElementById('id_content').value = SetkaEditor.getHTML({ includeContainer: true });
    document.getElementById('id_setla_layout_id').value = SetkaEditor.getCurrentLayout().id;
    document.getElementById('id_setka_theme_id').value = SetkaEditor.getCurrentTheme().id;
});

function getAllImages() {
    var result = {error: false, data: []}
    var request = new XMLHttpRequest();
    request.open('GET', '/setka/api/images/', true);
    request.send();
    request.onreadystatechange = function() {
        if (request.readyState != 4) return;
        if (request.status === 200) { 
            var response = JSON.parse(request.responseText);
            if ('postimages' in response) 
                result.data = response.postimages;
        } else {
            result.error = true;
        }
    };
    return result;
}
