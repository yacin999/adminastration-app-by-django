// $('#myModal').on('shown.bs.modal', function () {
//     $('#myInput').trigger('focus')
//   })

//   var sidebarColl = document.querySelector('#sidebarCollapse');
//   var sidebar = document.querySelector('#sidebar');
//   sidebarColl.addEventListener('click', () =>{
//       sidebar.classList.toggle('active');
//   });

// var modalButton = document.getElementById("staticBackdrop")

// modalButton.addEventListener("click", ()=>{
//     alert("bootstap button ckicked")
// })
const reserveBtn = document.querySelectorAll(".btn-reserve")
const returnMaterialBtn = document.querySelectorAll(".return-material-btn")


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



reserveBtn.forEach((element)=>{
    element.addEventListener("click", ()=>{
        let item_id = element.getAttribute('data-item-id')

        const url = 'http://127.0.0.1:8000/dashboard/new-order/'

        fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                id_of_material: item_id,
            })   
        }).then(res =>{
            if(res.ok){
                return res.json()
            }else {
                console.log("error")
            }
        }).then(data=>{
            console.log("data from serverside", data)
            window.location.href = "http://127.0.0.1:8000/dashboard/all-material/"
        })
        
    })    
})

returnMaterialBtn.forEach((btn)=>{
    btn.addEventListener('click',() =>{

        let item_id = btn.getAttribute('data-item')

        const url = 'http://127.0.0.1:8000/dashboard/return-material/'

        fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                id_of_material: item_id,
            })   
        }).then(res =>{
            if(res.ok){
                return res.json()
            }else {
                console.log("error")
            }
        }).then(data=>{
            console.log("data from serverside", data)
            window.location.href = "http://127.0.0.1:8000/dashboard/all-orders/"
        })


    })
})