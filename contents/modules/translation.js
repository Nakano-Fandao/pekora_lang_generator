const HOST = 'http://127.0.0.1:8080'

// Scrape sentences in web
const scrape = () => {
    const tag_array = ['p', 'li', 'th', 'td', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        .filter((tag) => (document.getElementsByTagName(tag).length != 0));

    const body_tag = ['p'];
    const sentence_dict = {'body': {}, 'headline': {}};

    tag_array.forEach(function(tag) {
        if ( body_tag.includes(tag) ) {
            sentence_dict['body'][tag] = [].concat(
                Array.from(document.getElementsByTagName(tag)).map(item => item.innerHTML));
        } else {
            sentence_dict['headline'][tag] = [].concat(
                Array.from(document.getElementsByTagName(tag)).map(item => item.innerHTML));
        }
    })
    return sentence_dict
}

// Ajax
const send_to_py = async (array) => {

    // Modules
    const removeLoading_module = await import("./loading.js");
    const updateAlmondStatus_module = await import("./almond_status.js");

    const data_to_python = JSON.stringify(array);
    console.log("Start Ajax request")
    $.ajax({
      type          : 'POST',
      url           : HOST + '/pekora',
      data          : data_to_python,
      contentType   : 'application/json'
    })
    .then(
        // Success
        data => {
            console.log("Ajax completed successfully!");

            // Replace sentence in the web page with pekora sentences
            const result = JSON.parse(data);
            replace_all(result.body);
            replace_all(result.headline);

            removeLoading_module.removeLoading();
            updateAlmondStatus_module.updateAlmondStatus("translation", true);
            console.log("Translation completed");
        },
        // Failure
        error => {
            alert('翻訳失敗ぺこ！！');
            console.log(error)
            removeLoading_module.removeLoading();
        }
    )
    .then( () => console.log("Data sending completed") );
}

// Replace sentences in web with pekora lang
function replace_all(dict) {
    const tags = Object.keys(dict)
    tags.forEach(function(tag) {
        const originals = document.getElementsByTagName(tag);
        const pekos = dict[tag];
        for (let i = 0; i < originals.length; i++) {
            originals[i].innerHTML = pekos[i];
        }
    })
}

const translate = () => {
    // Scrape body & headlines and create dictionary
    const sentence_dict = scrape();
    console.log("Scraping completed");

    // Send the dict to views.py
    send_to_py(sentence_dict);
}

const detranslate = () => {
    Promise.all([
        import("./loading.js"),
        import("./almond_status.js")
    ]).then( (modules) => {
        modules[0].removeLoading();
        modules[1].updateAlmondStatus("translation", false);
        console.log("Detranslation completed");
    });


}

export {translate, detranslate};
