const switch_imgs = () => {
    console.log("Switching images completed")
    import("../modules/loading.js").then( module => module.removeLoading() );
}

export {switch_imgs};
