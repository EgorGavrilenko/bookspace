var a = (function() {
  function set(e) {
    let evt = e || window.event;
    let current = evt.target || evt.srcElement;
    let doc = current.parentNode.parentNode;
    for (var i = 0; i < doc.childNodes.length; i++) {
      if (doc.childNodes[i].id == 'author') {
        author = doc.childNodes[i].textContent;
      }
      if (doc.childNodes[i].id == 'title') {
        title = doc.childNodes[i].textContent;
      }
      if (doc.childNodes[i].id == 'description') {
        description = doc.childNodes[i].textContent;
      }
      if (doc.childNodes[i].id == 'number_of_pages') {
        number_of_pages = parseInt(doc.childNodes[i].textContent);
      }
      if (doc.childNodes[i].id == 'price') {
        console.log(doc.childNodes[i].textContent.replace('$',''))
        price = parseInt(doc.childNodes[i].textContent.replace('$',''));
      }
    }
    newDescriptionAuthorLabel = document.getElementById('newDescriptionAuthorLabel');
    newDescriptionAuthorLabel.innerHTML = author;
    newDescriptionTitleLabel = document.getElementById('newDescriptionTitleLabel');
    newDescriptionTitleLabel.innerHTML = title;
    textOfDescription = document.getElementById('textOfDescription');
    textOfDescription.value = description;
    newDescriptionAuthor = document.getElementById('newDescriptionAuthor');
    newDescriptionAuthor.value = author;
    newDescriptionTitle = document.getElementById('newDescriptionTitle');
    newDescriptionTitle.value = title;
    newDescriptionNumberOfPages = document.getElementById('newDescriptionNumberOfPages');
    newDescriptionNumberOfPages.value = number_of_pages;
    newDescriptionPrice = document.getElementById('newDescriptionPrice');
    newDescriptionPrice.value = price;
  }

  return {
    set: set,
  };
})();
