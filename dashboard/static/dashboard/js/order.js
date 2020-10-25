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


// let module_inputs = document.querySelectorAll(".module-input")
let code_module = document.getElementById("code-module")
let name_module = document.getElementById("designation-module")
let credit_module = document.getElementById("credit-module")
let coeff_module = document.getElementById("coeff-module")
let cours_module = document.getElementById("cours-module")
let tp_module = document.getElementById("tp-module")
let td_module = document.getElementById("td-module")





// Module part_______________________________
try {
    code_module.addEventListener("blur", ()=>{

        fetch('http://127.0.0.1:8000/api/module-list')
        .then(res =>  res.json())
        .then( (module_data) => {
            let error_message = document.getElementById("error1")
            module_data.forEach(module =>{
                if(module.code === code_module.value){
                    error_message.innerHTML = `<i class="fas fa-exclamation-triangle text-danger mr-1"></i> le code de module déja existe`
                    error_message.hidden = false
                    error_message.style.cssText = "background: #ffdbdb;width: 211px;text-align: center;border-radius: 5px;"
                    code_module.style.cssText = "border: 2px solid #dc3545;border-radius: 5px;"
                }
            })
            if((code_module.value.length < 4 || code_module.value.length > 4) &&  code_module.value.length != 0) {
                let error_message = document.getElementById("error1")
                console.log("error", error_message)
                error_message.innerHTML = `<i class="fas fa-exclamation-triangle text-danger mr-1"></i> le code doit avoir au moins 4 longueurs`
                error_message.hidden = false
                error_message.style.cssText = "background: #ffdbdb;width: 211px;text-align: center;border-radius: 5px;"
                code_module.style.cssText = "border: 2px solid #dc3545;border-radius: 5px;"
            }
          })
    })
    code_module.addEventListener("focus", ()=>{
        let error_message = document.getElementById("error1")
        error_message.innerHTML = ""
        code_module.style.cssText = ""
    })


    name_module.addEventListener("blur", ()=>{
        fetch('http://127.0.0.1:8000/api/module-list')
        .then(res =>  res.json())
        .then( (module_data) => {
         
           for (let i = 0; i < module_data.length; i++) {
            if (module_data[i].designation === name_module.value) {
                let error_message = document.getElementById("error2")
                console.log("error", error_message)
                error_message.innerHTML =`<i class="fas fa-exclamation-triangle text-danger mr-1"></i> ce module existe déjà`
                error_message.hidden = false
                error_message.style.cssText = "background: #ffdbdb;width: 211px;text-align: center;border-radius: 5px"
                name_module.style.cssText = "border: 2px solid #dc3545;border-radius: 5px;"
            }
          }
          })
        .catch(err => console.log(err))
      
    
})
    name_module.addEventListener("focus", ()=>{
        let error_message = document.getElementById("error2")
        error_message.innerHTML = ""
        name_module.style.cssText = ""
    })


    credit_module.addEventListener("blur", ()=>{
        console.log("code_module.value" , credit_module.value)
        if(credit_module.value > 10) {
            let error_message = document.getElementById("error3")
            console.log("error", error_message)
            error_message.innerHTML = `<i class="fas fa-exclamation-triangle text-danger mr-1"></i> cette valeur ne doit pas passer le nombre 10`
            error_message.hidden = false
            error_message.style.cssText = "background: #ffdbdb;width: 211px;text-align: center;border-radius: 5px"
            credit_module.style.cssText = "border: 2px solid #dc3545;border-radius: 5px;"
        }
    })
    credit_module.addEventListener("focus", ()=>{
        let error_message = document.getElementById("error3")
        error_message.innerHTML = ""
        credit_module.style.cssText = ""
    })

    
    
    
    
    coeff_module.addEventListener("blur", ()=>{
    console.log("code_module.value" , coeff_module.value)
    if(coeff_module.value > 10) {
        let error_message = document.getElementById("error4")
        console.log("error", error_message)
        error_message.innerHTML = `<i class="fas fa-exclamation-triangle text-danger mr-1"></i> cette valeur ne doit pas passer le nombre 10`
        error_message.hidden = false
        error_message.style.cssText = "background: #ffdbdb;width: 211px;text-align: center;border-radius: 5px"
        coeff_module.style.cssText = "border: 2px solid #dc3545;border-radius: 5px;"
    }
})
    coeff_module.addEventListener("focus", ()=>{
        let error_message = document.getElementById("error4")
        error_message.innerHTML = ""
        coeff_module.style.cssText = ""
    })



    cours_module.addEventListener("blur", ()=>{
    console.log("code_module.value" , cours_module.value)
    if(cours_module.value > 10) {
        let error_message = document.getElementById("error5")
        console.log("error", error_message)
        error_message.innerHTML = `<i class="fas fa-exclamation-triangle text-danger mr-1"></i> cette valeur ne doit pas passer le nombre 10`
        error_message.hidden = false
        error_message.style.cssText = "background: #ffdbdb;width: 211px;text-align: center;border-radius: 5px"
        cours_module.style.cssText = "border: 2px solid #dc3545;border-radius: 5px;"
    }
})
    cours_module.addEventListener("focus", ()=>{
        let error_message = document.getElementById("error5")
        error_message.innerHTML = ""
        cours_module.style.cssText = ""
    })

    tp_module.addEventListener("blur", ()=>{
        console.log("code_module.value" , tp_module.value)
        if(tp_module.value > 10) {
            let error_message = document.getElementById("error6")
            console.log("error", error_message)
            error_message.innerHTML = `<i class="fas fa-exclamation-triangle text-danger mr-1"></i> cette valeur ne doit pas passer le nombre 10`
            error_message.hidden = false
            error_message.style.cssText = "background: #ffdbdb;width: 211px;text-align: center;border-radius: 5px"
            tp_module.style.cssText = "border: 2px solid #dc3545;border-radius: 5px;"
            
        }
    })
    tp_module.addEventListener("focus", ()=>{
        let error_message = document.getElementById("error6")
        error_message.innerHTML = ""
        tp_module.style.cssText = ""
    })


    td_module.addEventListener("blur", ()=>{
        console.log("code_module.value" , td_module.value)
        if(td_module.value > 10) {
            let error_message = document.getElementById("error7")
            error_message.innerHTML = `<i class="fas fa-exclamation-triangle text-danger mr-1"></i> cette valeur ne doit pas passer le nombre 10`
            error_message.hidden = false
            error_message.style.cssText = "background: #ffdbdb;width: 211px;text-align: center;border-radius: 5px"
            td_module.style.cssText = "border: 2px solid #dc3545;border-radius: 5px;"
        }
    })
    td_module.addEventListener("focus", ()=>{
        let error_message = document.getElementById("error7")
        error_message.innerHTML = ""
        td_module.style.cssText = ""
    })



} catch (error) {
}


// teacher input verification part_______________________________
try {
    let email_teacher = document.getElementById("email-teacher")
    let tel_teacher = document.getElementById("tel-teacher")
    let department = document.getElementById("department")

    department.addEventListener("change", ()=>{
        console.log("department has changed !!", department.value)
        if (department.value == 3) {
            console.log("hidden",document.getElementById("department2"), document.getElementById("department2").hidden )
            document.getElementById("department2").hidden = false
        }else{
            document.getElementById("department2").hidden = true
        }
    })

    email_teacher.addEventListener("blur", ()=>{
        console.log("code_module.value" , email_teacher.value)
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        // const re = /^[^@]+@(univ-mascara)\.dz$/i;
        let valid =  re.test(String(email_teacher.value).toLowerCase());

        if(!valid) {
            let error_message = document.getElementById("error1")
            console.log("error", error_message)
            error_message.innerHTML = `<i class="fas fa-exclamation-triangle text-danger mr-1"></i> cette email n'est pas valide`
            error_message.hidden = false
            error_message.style.cssText = "background: #ffdbdb;width: 211px;text-align: center;border-radius: 5px"
            email_teacher.style.cssText = "border: 2px solid #dc3545;border-radius: 5px;"

        }
    })
    email_teacher.addEventListener("focus", ()=>{
        let error_message = document.getElementById("error1")
        error_message.innerHTML = ""
        email_teacher.style.cssText = ""
    })

    // tel_teacher.addEventListener("blur", ()=>{
    //     const re = /^[(]{0,1}(213)[)]{0,1}[-\s\.]{0,1}[0-9]{3}[-\s\.]{0,1}[0-9]{4}$/;
    //     let valid =  re.test(tel_teacher.value)
    //     if(!valid) {
    //         let error_message = document.getElementById("error5")
    //         console.log("error", error_message)
    //         error_message.innerHTML = `<i class="fas fa-exclamation-triangle text-danger mr-1"></i> cette numero n'est pas valide`
    //         error_message.hidden = false
    //         error_message.style.cssText = "background: #ffdbdb;width: 211px;text-align: center;border-radius: 5px"
    //         tel_teacher.style.cssText = "border: 2px solid #dc3545;border-radius: 5px;"
    //     }
    // })
    // tel_teacher.addEventListener("focus", ()=>{
    //     let error_message = document.getElementById("error5")
    //     error_message.innerHTML = ""
    //     tel_teacher.style.cssText = ""
    // })


    
}catch{ 
}

// user input verification part_______________________________
try {
    
    let email_teacher = document.getElementById("email-user")
    console.log("order js", email_teacher)
    email_teacher.addEventListener("blur", ()=>{
        console.log("code_module.value" , email_teacher.value)
        const re = /^[^@]+@(univ-mascara)\.dz$/i;
        let valid =  re.test(String(email_teacher.value).toLowerCase());

        if(!valid) {
            let error_message = document.getElementById("error1")
            console.log("error", error_message)
            error_message.innerHTML = `<i class="fas fa-exclamation-triangle text-danger mr-1"></i> cette email n'est pas valide`
            error_message.hidden = false
            error_message.style.cssText = "background: #ffdbdb;width: 211px;text-align: center;border-radius: 5px"
            email_teacher.style.cssText = "border: 2px solid #dc3545;border-radius: 5px;"

        }
    })
    email_teacher.addEventListener("focus", ()=>{
        let error_message = document.getElementById("error1")
        error_message.innerHTML = ""
        email_teacher.style.cssText = ""
    })

} catch (error) {}


// anonymous user input verification part_______________________________
try {
    
    let email_anony = document.getElementById("id_email")
    email_anony.addEventListener("blur", ()=>{
        const re = /^[^@]+@(univ-mascara)\.dz$/i;
        let valid =  re.test(String(email_anony.value).toLowerCase());

        if(!valid) {
            let error_message = document.getElementById("error1")
            console.log("error", error_message)
            error_message.innerHTML = `<i class="fas fa-exclamation-triangle text-danger mr-1"></i> cette email n'est pas valide`
            error_message.hidden = false
            error_message.style.cssText = "background: #ffdbdb;width: 211px;text-align: center;border-radius: 5px"
            email_anony.style.cssText = "border: 2px solid #dc3545;border-radius: 5px;"

        }
    })
    email_anony.addEventListener("focus", ()=>{
        let error_message = document.getElementById("error1")
        error_message.innerHTML = ""
        email_anony.style.cssText = ""
    })

} catch (error) {}




// GETTING classroom document part &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

try {
    const level = document.getElementById("level")
    const table_id = document.getElementById("table")
    const semester = document.getElementById("semestre");
    const type = document.getElementById("type");
    const searchBtn= document.getElementById("search");
    const header = document.querySelector(".hint-header")
    

    level.addEventListener('change', (event) => {
    event.preventDefault();
    
    // var num_groups = document.getElementById("nbr-group");
    semester.innerHTML = "";
    semester.disabled = false;
    // num_groups.disabled = false;
    semester.innerHTML = "<option value='' selected disabled>-select-</option>"
    var option1 = document.createElement("option");
    var option2 = document.createElement("option");
    switch (level.value) {
      case "licence1":
      option1.textContent = "S1";
      option2.textContent = "S2";
      semester.appendChild(option1);
      semester.appendChild(option2);
      break;
      case "licence2":
      option1.textContent = "S3";
      option2.textContent = "S4";
      semester.appendChild(option1);
      semester.appendChild(option2);
      break;
      case "Licence3":
      option1.textContent = "S5";
      option2.textContent = "S6";
      semester.appendChild(option1);
      semester.appendChild(option2);
      break;
      case "Master1":
      option1.textContent = "M1";
      option2.textContent = "M2";
      semester.appendChild(option1);
      semester.appendChild(option2);
      break;
      case "Master2":
      option1.textContent = "M3";
      option2.textContent = "M4";
      semester.appendChild(option1);
      semester.appendChild(option2);
      break;
    }
  });


    searchBtn.addEventListener("click", ()=>{  
        if (level.value === "" || semester.value === "") {
            alert("vous devez sélectionner le niveau le semestre ")
            return 
        }

        fetch("http://127.0.0.1:8000/dashboard/load_document_cr_data",{
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                level : level.value,
                semester : semester.value,
                cr_type: type.value
            })   
        })
        .then(response=>response.json())
        .then((document_data)=>{
            if(document_data === "no result"){
                header.innerHTML = "pas de résultat"
                header.style.cssText = `
                color: #fff;
                padding: 20px 10px;
                background-color: #ff3d3d;
                text-align: center;
                width: 50%;
                margin-left: 25%;
                border-radius: 5px;
                `
                table_id.innerHTML = ""
            }else{

                let timetable_container = `
            <table class="table">
                <thead class="thead">
                <tr>
                <th scope="col">Jour</th>
                <th scope="col">Heure</th>
                <th scope="col">Groupe</th>
                <th scope="col">Type</th>
                <th scope="col">Salle</th>
                </tr>
                </thead>
                <tbody id="body-table">
                </tbody>
            </table>

        `
                table_id.innerHTML = timetable_container

                // var message = document.querySelector(".hint-header")
                header.innerHTML = ""
                header.style.cssText = ""

                let table_body = document.getElementById("body-table")
                table_body.innerHTML = ""

                var document_data_array = Object.values(document_data)
                for (let i = 0; i< document_data_array.length; i++) {
                    table_body.innerHTML += `
                        <tr>
                        <th scope="row">${document_data_array[i].day}</th>
                        <td>${document_data_array[i].hour}</td>
                        <td>${document_data_array[i].group}</td>
                        <td>${document_data_array[i].type}</td>
                        <td>${document_data_array[i].classroom}</td>
                        </tr>
                    `
                }

                document.getElementById("pdf-btn").hidden = false
                document.getElementById("url-anchor").setAttribute("href", `/dashboard/${level.value}-${semester.value}-${type.value}/cr-tt/pdf`)
                console.log("our pdf btn", document.getElementById("pdf-btn"))
            }
        })
    })

} catch (error) {
    console.log("")
}

// teaching followup document ======================================================
try {

    const level = document.getElementById("level")
    const table_id = document.getElementById("table")
    const semester = document.getElementById("semestre");
    const searchBtn_teaching_followup = document.getElementById("search-Tfollowup");
    const header = document.querySelector(".hint-header")


    level.addEventListener('change', (event) => {
        event.preventDefault();
        
        // var num_groups = document.getElementById("nbr-group");
        semester.innerHTML = "";
        semester.disabled = false;
        // num_groups.disabled = false;
        semester.innerHTML = "<option value='' selected disabled>-select-</option>"
        var option1 = document.createElement("option");
        var option2 = document.createElement("option");
        switch (level.value) {
          case "licence1":
          option1.textContent = "S1";
          option2.textContent = "S2";
          semester.appendChild(option1);
          semester.appendChild(option2);
          break;
          case "licence2":
          option1.textContent = "S3";
          option2.textContent = "S4";
          semester.appendChild(option1);
          semester.appendChild(option2);
          break;
          case "Licence3":
          option1.textContent = "S5";
          option2.textContent = "S6";
          semester.appendChild(option1);
          semester.appendChild(option2);
          break;
          case "Master1":
          option1.textContent = "M1";
          option2.textContent = "M2";
          semester.appendChild(option1);
          semester.appendChild(option2);
          break;
          case "Master2":
          option1.textContent = "M3";
          option2.textContent = "M4";
          semester.appendChild(option1);
          semester.appendChild(option2);
          break;
        }
      });
    
      searchBtn_teaching_followup.addEventListener("click", ()=>{  
        if (level.value === "" || semester.value === "") {
            alert("vous devez sélectionner le niveau le semestre ")
            return 
        }

        fetch("http://127.0.0.1:8000/dashboard/load-document-tf",{
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                level : level.value,
                semester : semester.value,
            })   
        })
        .then(response=>response.json())
        .then((document_data)=>{
            if(document_data === "no result"){
                header.innerHTML = "pas de résultat"
                header.style.cssText = `
                color: #fff;
                padding: 20px 10px;
                background-color: #ff3d3d;
                text-align: center;
                width: 50%;
                margin-left: 25%;
                border-radius: 5px;
                `
                table_id.innerHTML = ""
            }else{

                let timetable_container = `
            <table class="table">
                <thead class="thead">
                <tr>
                    <th scope="col">Jour</th>
                    <th scope="col">Heure</th>
                    <th scope="col">Groupe</th>
                    <th scope="col">Module</th>
                    <th scope="col">Nature</th>
                    <th scope="col">Enseignant</th>
                    <th scope="col">Salle</th>
                </tr>
                </thead>
                <tbody id="body-table">
                
                </tbody>
                </table>
            `
                table_id.innerHTML = timetable_container

                // var message = document.querySelector(".hint-header")
                header.innerHTML = ""
                header.style.cssText = ""

                let table_body = document.getElementById("body-table")
                table_body.innerHTML = ""

                var document_data_array = Object.values(document_data)
                for (let i = 0; i< document_data_array.length; i++) {
                    table_body.innerHTML += `
                        <tr>
                            <th scope="row">${document_data_array[i].day}</th>
                            <td>${document_data_array[i].hour}</td>
                            <td>${document_data_array[i].group}</td>
                            <td>${document_data_array[i].module}</td>
                            <td>${document_data_array[i].nature}</td>
                            <td>${document_data_array[i].teacher}</td>
                            <td>${document_data_array[i].classroom}</td>
                        </tr>
                    `
                }

                document.getElementById("pdf-btn").hidden = false
                document.getElementById("url-anchor").setAttribute("href", `/dashboard/${level.value}-${semester.value}/weekly-followup/pdf`)
                console.log("our pdf btn", document.getElementById("pdf-btn"))
            }
        })
    })

} catch (error) {}


// teacher hourly Loader ===========================================================
try {
    // const level = document.getElementById("level")
    // const semester = document.getElementById("semestre");
    const table_id = document.getElementById("table")
    const searchBtn_teacher_hourlyL = document.getElementById("searchBtn_teacher_hourlyL");
    const header = document.querySelector(".hint-header")
    const department = document.getElementById("depart")

   
    searchBtn_teacher_hourlyL.addEventListener("click", ()=>{  
        // if (level.value === "" || semester.value === "") {
        //     alert("vous devez sélectionner le niveau le semestre ")
        //     return 
        // }

        fetch("http://127.0.0.1:8000/dashboard/load-document-tl",{
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                department : department.value
            })   
        })
        .then(response=>response.json())
        .then((document_data)=>{
            console.log("teacher hourly", document_data)
            if(document_data === "no result"){
                header.innerHTML = "pas de résultat"
                header.style.cssText = `
                color: #fff;
                padding: 20px 10px;
                background-color: #ff3d3d;
                text-align: center;
                width: 50%;
                margin-left: 25%;
                border-radius: 5px;
                `
                table_id.innerHTML = ""
                document.getElementById("pdf-btn").hidden = true
            }else{

                let timetable_container = `
            <table class="table">
                <thead class="thead">
                <tr>
                    <th scope="col">Enseignant</th>
                    <th scope="col">Module</th>
                    <th scope="col">Nature</th>
                    <th scope="col">Groupe</th>
                    <th scope="col">Charge horaire</th>
                </tr>
                </thead>
                <tbody id="body-table">
                </tbody>
            </table>

        `
                table_id.innerHTML = timetable_container

                // var message = document.querySelector(".hint-header")
                header.innerHTML = ""
                header.style.cssText = ""

                let table_body = document.getElementById("body-table")
                table_body.innerHTML = ""

                var document_data_array = Object.entries(document_data)
                console.log("list ", document_data_array)

                for (let i = 0; i < document_data_array.length; i++) {
                    table_body.innerHTML += `
                    <tr>
                        <td>${document_data_array[i][0]}</td>
                        <td>${document_data_array[i][1].module}</td>
                        <td>${document_data_array[i][1].nature}</td>
                        <td>${document_data_array[i][1].group}</td>
                        <td>${document_data_array[i][1].count} séance</td>
                    </tr>
                `                     
                }

                document.getElementById("pdf-btn").hidden = false
                document.getElementById("url-anchor").setAttribute("href", `/dashboard/${department.value}/t-hourlyL/pdf`)
                console.log("our pdf btn", document.getElementById("pdf-btn"))
                
               
            }
        })
    })



} catch (error) {}



// teacher department DOCUMENT ==============================================================
try {
    const table_id = document.getElementById("table")
    const searchBtn_teacher_department = document.getElementById("searchBtn_teacher_department");
    const header = document.querySelector(".hint-header")


    searchBtn_teacher_department.addEventListener("click", ()=>{  
        

        fetch("http://127.0.0.1:8000/dashboard/load-teacher-department",{
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                department : department.value
            })   
        })
        .then(response=>response.json())
        .then((document_data)=>{
            console.log("document", document_data)
            if(document_data === "no result"){
                console.log("no result");
                header.innerHTML = "pas de résultat"
                header.style.cssText = `
                color: #fff;
                padding: 20px 10px;
                background-color: #ff3d3d;
                text-align: center;
                width: 50%;
                margin-left: 25%;
                border-radius: 5px;
                `
                table_id.innerHTML = ""
            }else{

                let timetable_container = `
            <table class="table">
                <thead class="thead">
                <tr>
                    <th scope="col">Enseignant</th>
                    <th scope="col">Email</th>
                </tr>
                </thead>
                <tbody id="body-table">
                </tbody>
            </table>

        `
                table_id.innerHTML = timetable_container
                header.innerHTML = ""
                header.style.cssText = ""

                let table_body = document.getElementById("body-table")
                table_body.innerHTML = ""

                var document_data_array = Object.values(document_data)
                for (let i = 0; i< document_data_array.length; i++) {
                    table_body.innerHTML += `
                        <tr>
                            <th scope="row">${document_data_array[i].teacher}</th>
                            <td>${document_data_array[i].email}</td>
                        </tr>
                    `
                }
            }
        })
    })

} catch (error) {}


// timetable of teacher DOCUMENT ==============================================================
try {
    const table_id = document.querySelector(".our_table")
    const searchBtn_tt_teacher = document.getElementById("searchBtn_tt_teacher");
    const header = document.querySelector(".hint-header")
    const teacher = document.getElementById("teacher")



    function searchIn_select(parent, val) {
        for (var i=0; i <parent.length; i++) {
          if (parent.querySelectorAll("option")[i].value === val) {
            return parent.querySelectorAll("option")[i];
          }
        }
    }


    searchBtn_tt_teacher.addEventListener("click", ()=>{  

        let slug_t = searchIn_select(teacher, teacher.value)
        console.log("our slug is", slug_t.getAttribute("data-teacher-slug"))
        

        fetch("http://127.0.0.1:8000/dashboard/load-teacher-timetable",{
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                slug : slug_t.getAttribute("data-teacher-slug")
            })   
        })
        .then(response=>response.json())
        .then((document_data)=>{

            console.log("document", document_data)
            if(document_data === "no result"){
                console.log("no result");
                header.innerHTML = "pas de résultat"
                header.style.cssText = `
                color: #fff;
                padding: 20px 10px;
                background-color: #ff3d3d;
                text-align: center;
                width: 50%;
                margin-left: 25%;
                border-radius: 5px;
                `
                table_id.innerHTML = ""
            }else{

                let timetable_container = `
                <div class="our_row">
                    <span class="our_cell times">days</span>
                    <span class="our_cell times">8:30 - 10:00</span>
                    <span class="our_cell times">10:15 - 11:45</span>
                    <span class="our_cell times">11:45 - 13:30</span>
                    <span class="our_cell times">13:30 - 15:00</span>
                    <span class="our_cell times">15:00 - 16:30</span>
                </div>
                `
                table_id.innerHTML = timetable_container
                header.innerHTML = ""
                header.style.cssText = ""

                var document_data_array = Object.values(document_data)
                for (let i = 0; i< document_data_array.length; i++) {
                    table_id.innerHTML += `
                        <tr>
                            <th scope="row">${document_data_array[i].teacher}</th>
                            <td>${document_data_array[i].email}</td>
                        </tr>
                    `
                }
            }
        })
    
    })

} catch (error) {}
