var a = (function() {
  function addUser() {
    addU(document.getElementById('newUserName').value)
      .then(result => {
        location.reload();
      })
      .catch(err => {
        alert(err.error);
      });
  }

  function addU(name) {
    return new Promise(function(resolve, reject) {
      let xhr = new window.XMLHttpRequest();
      let body = 'name=' + encodeURIComponent(name);
      xhr.open('POST', '/api/addUser', true);
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

  return {
    addUser: addUser,
    getBooks: getBooks,
  };
})();
