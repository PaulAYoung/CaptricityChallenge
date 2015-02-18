function imageLoader(page, imageDiv, api){
    this._page = page;
    this._imageDiv = $(imageDiv);
    this._api = api;
    this._getImages();
}

imageLoader.prototype._getImages = function(page){
    if (typeof page === 'undefined'){page=this._page}
    $.get(this._api, {page: page}, $.proxy(this._fillImages, this))
};

imageLoader.prototype._fillImages=function(data){
    this._imageDiv.empty();
    var images=data.images;
    var html, title, url, page, batchStatus;
    for (var i=0; i<images.length; i++){
        title = images[i].title;
        page = images[i].page;
        url = images[i].url;
        batchStatus = images[i].status;
        if (batchStatus=== null){batchStatus="Unprocessed";}
        html = '<div class="col-md-2 image_thumb">' +
            '<a href="' + page + '">' + title + 
            '<img class="img-thumbnail" src="' + url + '" alt="' + title + '"><br>' +
            '</a>' +
            "<br>Status: " + batchStatus +
            '</div>';

        this._imageDiv.append(html);
            
    }
};
