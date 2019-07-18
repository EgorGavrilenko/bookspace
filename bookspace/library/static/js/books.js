var a = (function() {
  let author;
  let title;
  let description;
  let price;
  let number_of_pages;
  function addBook() {
    addB(
      document.getElementById('name').textContent,
      document.getElementById('authorOfTheBookBeingAdded').value,
      document.getElementById('titleOfTheBookBeingAdded').value,
      document.getElementById('descriptionOfTheBookBeingAdded').value
    ).then(
      result => {
        location.reload();
      },
      err => {
        alert('add error');
      }
    );
  }

  function addB(name, author, title, description) {
    return new Promise(function(resolve, reject) {
      let xhr = new window.XMLHttpRequest();
      let body =
        'name=' +
        encodeURIComponent(name) +
        '&author=' +
        encodeURIComponent(author) +
        '&title=' +
        encodeURIComponent(title) +
        '&description=' +
        encodeURIComponent(description);
      xhr.open('POST', '/api/assignBook', true);
      xhr.responseType = 'document';
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
      xhr.onload = function() {
        if (this.status === 200) {
          resolve(this.response);
        } else {
          var error = new Error(this.statusText);
          error.code = this.status;
          reject(error);
        }
      };
      xhr.send(body);
    });
  }

  function getBooks(id) {
    let loc = window.location;
    window.location = window.location + 'api/getBooks?name=' + id;
  }

  function editDescription() {
    editD(
      document.getElementById('name').textContent,
      author,
      title,
      document.getElementById('textOfDescription').value
    ).then(
      result => {
        location.reload();
      },
      err => {
        alert('edit error');
      }
    );
  }

  function editD(name, author, title, description) {
    return new Promise(function(resolve, reject) {
      let xhr = new window.XMLHttpRequest();
      let body =
        'name=' +
        encodeURIComponent(name) +
        '&author=' +
        encodeURIComponent(author) +
        '&title=' +
        encodeURIComponent(title) +
        '&description=' +
        encodeURIComponent(description)+
        '&price=' +
        encodeURIComponent(price)+
        '&number_of_pages=' +
        encodeURIComponent(number_of_pages);

      xhr.open('POST', '/api/editDescription', true);
      xhr.responseType = 'document';
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
      xhr.onload = function() {
        if (this.status === 200) {
          resolve(this.response);
        } else {
          var error = new Error(this.statusText);
          error.code = this.status;
          reject(error);
        }
      };
      xhr.send(body);
    });
  }

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
    newDescriptionAuthor = document.getElementById('newDescriptionAuthor');
    newDescriptionAuthor.innerHTML = author;
    newDescriptionTitle = document.getElementById('newDescriptionTitle');
    newDescriptionTitle.innerHTML = title;
    textOfDescription = document.getElementById('textOfDescription');
    textOfDescription.value = description;
  }

  return {
    addBook: addBook,
    set: set,
    getBooks: getBooks,
    editDescription: editDescription,
  };
})();
