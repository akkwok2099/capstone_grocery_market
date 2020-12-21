/*************************/
/******  General  ********/
/*************************/

function getHeaders() {
    var token = "";

    if(document.getElementsByName("access").length > 0) {
        token = document.getElementsByName("access")[0].textContent;
    }
    
    return {
        "Content-type": "application/json;charset=UTF-8",
        "Authorization": "bearer " + token
    }
}

/**********************/
/******  Aisles  ******/
/**********************/

function deleteAisle(e, id) {
    e.preventDefault;

    isCertain = confirm('Are you sure you want to delete Aisle ' + id + '?')

    if(isCertain) {
    
        console.log('Start deleting aisle');
  
        fetch('/aisles/' + id, {
            method: 'DELETE',
            headers: getHeaders()
        }).then(response => {
            window.location.reload(false);
        });
    }
}
