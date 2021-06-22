const usePekoraCursor = () => {
    const cursor_dir = chrome.extension.getURL("../images/cursors/")
    const arrowUrl = cursor_dir + "pekora_arrow.png";
    const pointerUrl = cursor_dir + "carrot_pointer.png";

    // 通常カーソル
    $("body").css("cursor", "URL('" + arrowUrl + "'), auto");

    // なにかにhover時カーソル
    const pointer_tag = ["a", "button", "label a"];
    pointer_tag.map( tag => $(tag).css("cursor", "URL('" + pointerUrl + "'), pointer") );

    Promise.all([
        import("./loading.js"),
        import("./almond_status.js")
    ]).then( (modules) => {
        modules[0].removeLoading();
        modules[1].updateAlmondStatus("cursor", true);
    });
    console.log("Activate Pekora cursor");
}

const removePekoraCursor = () => {
    $("body").css("cursor", "auto");

    Promise.all([
        import("./loading.js"),
        import("./almond_status.js")
    ]).then( (modules) => {
        modules[0].removeLoading();
        modules[1].updateAlmondStatus("cursor", false);
    });
    console.log("Deactivate Pekora cursor");
}

export {usePekoraCursor, removePekoraCursor};
