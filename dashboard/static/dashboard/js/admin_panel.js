
// SIDEBARE COLLAPSE ANIMATION  8888888888888888888888

var sidebarColl = document.querySelector('#sidebarCollapse');
var sidebar = document.querySelector('#sidebar');
var sideBarButton = document.getElementById("sidebarCollapse");
var wrapper = document.getElementById("wrapper");
var notification_icon = document.getElementById("notification-btn")
var admin_icon = document.getElementById("profile-img")
var notification_dropdown_list = document.querySelector(".bell-dropdown-list")
var admin_icon_dropdown_list = document.querySelector(".profile-dropdown-list")
var dropdown_btn = document.getElementsByClassName("dropdown-btn")
var notif_confirm_btn = document.querySelectorAll(".notif-confirm")
var notif_delete_btn = document.querySelectorAll(".notif-suprimer")
var navbar_links = document.querySelectorAll(".sidebar-links")


sidebarColl.addEventListener('click', () =>{
    sidebar.classList.toggle('active');
});


sideBarButton.addEventListener('click', function () {
  wrapper.classList.toggle("wrapper");            
});





if(document.getElementById("notification-btn")!= null){
    admin_icon.addEventListener("click", ()=> {
        if(admin_icon_dropdown_list.style.display === "block"){
            admin_icon_dropdown_list.style.display = "none"
        }else{
            admin_icon_dropdown_list.style.display = "block"
        }
    })

    notification_icon.addEventListener("click", ()=> {
        if(notification_dropdown_list.style.display === "block"){
            notification_dropdown_list.style.display = "none"
        }else{
            notification_dropdown_list.style.display = "block"
        }
    })

    //canceling dropdown if the user clicked anywhere 
    window.addEventListener('click', (e)=>{
        
        if(e.target.id !== "profile-img"){
            // alert('first')
            if(admin_icon_dropdown_list.style.display === "block"){
                admin_icon_dropdown_list.style.display = "none"
            }
        }

        if(e.target.id !== "notification-btn"){
                if(notification_dropdown_list.style.display === "block"){
                    notification_dropdown_list.style.display = "none"
                }
        }
    })
}else{
    admin_icon.addEventListener("click", ()=> {
        if(admin_icon_dropdown_list.style.display === "block"){
            admin_icon_dropdown_list.style.display = "none"
        }else{
            admin_icon_dropdown_list.style.display = "block"
        }
    })

    window.addEventListener('click', (e)=>{
        
        if(e.target.id !== "profile-img"){
            // alert('first')
            if(admin_icon_dropdown_list.style.display === "block"){
                admin_icon_dropdown_list.style.display = "none"
            }
        }
    })

}







//_dropdown OF SIDE BAR and setting session function-------------------------

// var dropdownIsOpen;
var dropdownIsOpen = {}
var openDropDownOnLoad = {}

var linkIsFocus = {}
var focuslinkOnLoad = {}


for(let i=0; i<dropdown_btn.length; i++){
    openDropDownOnLoad[`${i}`] = false;
}
for(let i=0; i<navbar_links.length; i++){
    focuslinkOnLoad[`${i}`] = false
}



for(let i=0; i<dropdown_btn.length; i++){

    function toggleDropdown() {
        dropdownIsOpen[`${i}`] = !dropdownIsOpen[`${i}`]
        
        // Check if the sidebar should be open
        if (dropdownIsOpen[`${i}`]) {
      
            let dropdown_container = dropdown_btn[i].nextElementSibling
            dropdown_btn[i].firstChild.style.transform = "rotate(90deg)"
            dropdown_container.style.display = "block"
            dropdown_container.style.transition = "all 300 ease 300"
       
            localStorage.setItem(`button ${i}`, 'block');

          // And send a message to the console to let us know...
      
        } else {
      
            let dropdown_container = dropdown_btn[i].nextElementSibling
            dropdown_btn[i].firstChild.style.transform = ""
            dropdown_container.style.display = "none"
            dropdown_container.style.transition = "all 300 ease 300"
      
          // Now set the storage item to "closed"...
          localStorage.setItem(`button ${i}`, 'none');
      
          // And send a message to the console to let us know...
        //   console.log('The \'closed\' storage item has been set.');
      
        }
    }
      

      // Next we'll need to check if the storage item exists at all
    if (localStorage.getItem(`button ${i}`) === null) {

        // dropdownIsOpen = openDropDownOnLoad;
        dropdownIsOpen[`${i}`] = openDropDownOnLoad[`${i}`];
        
        
        // And send a message to the console to let us know...
        // console.log('The default state is ' + openDropDownOnLoad[`${i}`]);
        
        } else {
        
        // If the storage item does exist, and the value is set to "opened"...
            if (localStorage.getItem(`button ${i}`) === 'block') {
        
                // Set the state to open
                // dropdownIsOpen = true;
                dropdownIsOpen[`${i}`] = true
        
                // And send a message to the console to let us know...
                // console.log('The \'opened\' storage item is set; the sidebar should be open.');
        
            } else {
        
                // Otherwise, the value should be "closed"; set the state accordingly
                //dropdownIsOpen = false;
                dropdownIsOpen[`${i}`] = false
            
                // And send a message to the console to let us know...
                // console.log('The \'closed\' storage item is set; the sidebar should be closed.');
        
            }
    }
        
    
    
    // Does the "opened" storage item exist, or is the default state true?
    if (dropdownIsOpen[`${i}`]) {
    
        let dropdown_container = dropdown_btn[i].nextElementSibling
        dropdown_container.style.display = "block";
        dropdown_container.style.transition = "all 300 ease 300"
        dropdown_btn[i].firstChild.style.transform = "rotate(90deg)"
        
        // Let's have the console tell us what's happening...
        // console.log('The \'open-on-load\' class has been added.');
    
    }
    
    

    
    dropdown_btn[i].addEventListener('click', toggleDropdown)
}


// for(let i=0; i<navbar_links.length; i++) {
//     function link_focus () {
//         linkIsFocus[`${i}`] = !linkIsFocus[`${i}`]
        
//         // Check if the sidebar should be open
//         if (linkIsFocus[`${i}`]) {
            
//             navbar_links[i].style.color = "#EBE70F"
       
//             localStorage.setItem(`link ${i}`, 'focus');
         
//           console.log('The \'opened\' storage item has been set.');
      
//         } else {
      
//             navbar_links[i].style.color = "#FFF"
      
//           localStorage.setItem(`link ${i}`, 'not focus');
      
//           console.log('The \'closed\' storage item has been set.');
      
//         }
//     }


//     if (localStorage.getItem(`link ${i}`) === null) {

//         linkIsFocus[`${i}`] = focuslinkOnLoad[`${i}`];
        
    
        
//         } else {
        
//         // If the storage item does exist, and the value is set to "opened"...
//             if (localStorage.getItem(`link ${i}`) === 'focus') {
//                 linkIsFocus[`${i}`] = true
//             } else {
        
//                 // Otherwise, the value should be "closed"; set the state accordingly
//                 linkIsFocus[`${i}`] = false
            
        
//             }
//     }


//     // Does the "opened" storage item exist, or is the default state true?
//     if (linkIsFocus[`${i}`]) {
    
//         navbar_links[i].style.color = "#EBE70F";
            
//     }

//     navbar_links[i].addEventListener('click', link_focus)
// }


















// for(let i=0; i<dropdown_btn.length; i++){
//   dropdown_btn[i].addEventListener("click", ()=>{
//     dropdown_btn[i].classList.toggle("active")
//     let dropdown_container = dropdown_btn[i].nextElementSibling
//     if(dropdown_container.style.display === ""){
//         dropdown_container.style.display = "none"
//     }

//     console.log("dropdown container", dropdown_container, dropdown_container.style.display)
//     sessionStorage.setItem(`button ${i}`, dropdown_container.style.display)
//     var dropdown_stats = sessionStorage.getItem(`button ${i}`)
//     // console.log("dropdown_stats", sessionStorage.getItem(`button ${i}`))

//     if(dropdown_stats === "block"){
//         //sessionStorage.setItem("dropdown_status, block")

//       dropdown_container.style.display = "none"
//       dropdown_btn[i].firstChild.style.transform = ""
//     }else{
//       //sessionStorage.setItem("display, block")
//       dropdown_container.style.display = "block"
//       dropdown_btn[i].firstChild.style.transform = "rotate(90deg)"
//       //dropdown_container.style.transition = " 2s;"
      
//     }
    
//   })            
// }


// window.addEventListener("beforeunload", () => {
//     sessionStorage.setItem(`button ${index}`, "block");
//     dropdown_btn[index].style.display = "block"
//     // console.log("before loading")
// });

// window.addEventListener("beforeunload", () => {
//     sessionStorage.setItem("", sidebar.scrollTop);
// });

// document.onreadystatechange = () => {
//     if (document.readyState === 'complete') {
//         console.log("document is ready")
//         for (let index = 0; index < sessionStorage.length; index++) {
//             console.log("localStorage[`button ${index}`] ", sessionStorage.getItem(`button ${index}`))
//             if(sessionStorage.getItem(`button ${index}`) === "block"){
//                 dropdown_btn[index].style.display = "block"
//             }
//         }
        
//     }
//   };










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

// accepting or deleting new user accounts
notif_confirm_btn.forEach(element=>{
    element.addEventListener("click", ()=>{
        const account_id = document.getElementById("account-id")
        url = "http://127.0.0.1:8000/dashboard/confirm-anony-user/"
        fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                "account_id": account_id.getAttribute("data-account-id"),
                "operation": "confirm",

            })
        })
        .then(res=>res.json())
        .then(msg=>{
            console.log(msg)
            window.location.href = "http://127.0.0.1:8000/dashboard/"
        })
    })
})

notif_delete_btn.forEach(element=>{
    element.addEventListener("click", ()=>{
        const account_id = document.getElementById("account-id")
        url = "http://127.0.0.1:8000/dashboard/confirm-anony-user/"
        fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                "account_id": account_id.getAttribute("data-account-id"),
                "operation": "delete"
            })
        })
        .then(res=>res.json())
        .then(msg=>{
            console.log(msg)
            window.location.href = "http://127.0.0.1:8000/dashboard/"
        })
    })
})


