var a = (function() {

  let name;
  function set(e) {
    let evt = e || window.event;
    let current = evt.target || evt.srcElement;
    let doc = current.parentNode.parentNode;
    console.log(doc);
    for (var i = 0; i < doc.childNodes.length; i++) {
      if (doc.childNodes[i].id == 'name') {
        name = doc.childNodes[i].textContent;
      }
    }
    newImgUser = document.getElementById('newImgUser');
    newImgUser.innerHTML = name;
    newImgUser = document.getElementById('nameForEditImg');
    newImgUser.value = name;
  }

  return {
    set: set
  };
})();
