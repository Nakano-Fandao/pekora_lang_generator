const switch_imgs = () => {
    console.log("Switching images completed")
    import("./loading.js").then( module => module.removeLoading() );
    import("./almond_status.js")
        .then( module => module.updateAlmondStatus("images", true) );
}

const returnOriginalImgs = () => {
    import("./almond_status.js")
        .then( module => module.updateAlmondStatus("images", false) );

}

export {switch_imgs, returnOriginalImgs};
