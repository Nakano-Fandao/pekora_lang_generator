const usePekoraCursor = () => {
    const cursor_dir = chrome.extension.getURL("../images/cursors/")
    const arrowUrl = cursor_dir + "pekora_arrow.png";
    const pointerUrl = cursor_dir + "carrot_pointer.png";

    // 通常カーソル
    $("body").css("cursor", "URL('" + arrowUrl + "'), auto");

    // なにかにhover時カーソル
    const pointer_tag = ["a", "button", "label a"];
    pointer_tag.map( tag => $(tag).css("cursor", "URL('" + pointerUrl + "'), pointer") );

    import("./loading.js").then( module => module.removeLoading() );
    import("./almond_status.js")
        .then( module => module.updateAlmondStatus("cursor", true) );
    console.log("Activate Pekora cursor");
}

const removePekoraCursor = () => {
    $("body").css("cursor", "auto");
    import("./loading.js").then( module => module.removeLoading() );
    import("./almond_status.js")
        .then( module => module.updateAlmondStatus("cursor", false) );
    console.log("Deactivate Pekora cursor");
}

export {usePekoraCursor, removePekoraCursor};
