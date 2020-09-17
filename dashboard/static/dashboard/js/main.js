//............................
//. GLOGAL VARIABLES         .
//............................                

let dataObject = {};
let counters_module_TP = {};
let counters_module_TD = {};
let counters_module_Cours = {};
let event_period = {};
let id_event = "";
let cours_was_submitted = false
let tdp_was_submitted = false
// this variable is for listening to users clicks on the timetable
const targets = document.querySelectorAll(".our_target");
const td_cours_btn = document.getElementById("choise");
const nmb_g_buttn = document.getElementById("R-numb-btn");
const sub_table_btn = document.getElementById("create");


// function return_user_inputs() {
//   const user_inputs = document.querySelectorAll(".period-select");
//   return user_inputs
// }


// async function wrapper() {
//   const userinput = await return_user_inputs()
    
//     console.log("all inputs : ", user_inputs)
//   }
// }





// this try catch block is to avoid an error caused by unloaded template
try {
  targets.forEach(target => {target.addEventListener("click", period_tb_click)});

  td_cours_btn.addEventListener("click", td_cr_click);

  nmb_g_buttn.addEventListener("click", nbr_group_click);
 
  sub_table_btn.addEventListener("click", ()=>{
    const td_cours_choise = document.getElementById("select-TD-cours")
    const nmb_group = document.querySelector("#group-numb-input");
    const cansel = check_empty_input()

    // IF there any empty user's input then cancel submitting data to table
    if (cansel) {return}
  
    if(td_cours_choise.value === "TD-TP") {

      //inserting data to table period and saving them in our global object
      insertPeriodT(parseInt(nmb_group.textContent), event_period, id_event, dataObject, td_cours_choise.value); 
      
      // hiding number of groups part and show td/cours selection
      document.querySelector(".hidden-part").hidden = true
      document.querySelector(".row.pb").hidden = false  
      
      
      // hiding popup window after submiting the data
      $('#exampleModall').modal('hide');    
  
    }else if(td_cours_choise.value === "Cours"){

      //inserting data to table period and saving them in our global object
      insertPeriodC(event_period, id_event, dataObject, td_cours_choise.value);
  
      // hiding popup window after submiting the data
      $('#exampleModall').modal('hide');
    }
  });
  
} catch (error) {
  // alert('the button was clicked by mistake')
  console.log("the specified template didn't load yet !!: ", error)
}










//===================//---------------------------------||===============================
//======================//  functions's declaration part    ||===============================
//===================//---------------------------------||===============================

// reset function:
function resetInputs() {
  console.log("from reset FUNCTION //")
  document.getElementById('creates').innerHTML='';    
  $('#select-TD-cours').val('');                            
}
//Function to search inside a particular select_option html element:
function searchIn_select(parent, val) {
  for (var i=0; i <parent.length; i++) {
    if (parent.querySelectorAll("option")[i].value === val) {
      return parent.querySelectorAll("option")[i];
    }
  }
}
  

//Function to fetch module API :______________________________________________________________
function module_api(our_element, first_child) {
  var levelValue = document.getElementById("level").value;
  var semestreValue = document.getElementById("semestre").value;
  fetch('http://127.0.0.1:8000/api/module-list')
  .then(res =>  res.json())
  .then( (module_data) => {
    our_element.appendChild(first_child);
     for (let i = 0; i < module_data.length; i++) {
      var another_option = document.createElement('option');
      if (module_data[i].niveau.Nv === levelValue) {
        another_option.textContent = `${module_data[i].designation}`;
        another_option.setAttribute(`value`, `${module_data[i].designation}`);
        our_element.appendChild(another_option);
      }
    }
    })
  .catch(err => console.log(err))
}
//Function to fetch teacher API :______________________________________________________________
function teacher_api(our_element, first_child) {
  fetch('http://127.0.0.1:8000/api/teacher-list')
  .then(res =>  res.json())
  .then( (teacher_data) => {
    //console.log("teacher data" ,teacher_data)
    our_element.appendChild(first_child);
     for (let i = 0; i < teacher_data.length; i++) {
      var other_option = document.createElement('option');    
        other_option.textContent = `${teacher_data[i].nom}`;
        other_option.setAttribute(`value`, `${teacher_data[i].nom}`);
        our_element.appendChild(other_option);
    }
    })
  .catch(err => console.log(err))
}
//Function to fetch classroom API :______________________________________________________________
function classroom_api(our_element, first_child) {
  fetch('http://127.0.0.1:8000/api/classroom-list')
  .then(res =>  res.json())
  .then( (classroom_data) => {
    our_element.appendChild(first_child);
     for (let i = 0; i < classroom_data.length; i++) {
      var other_option = document.createElement('option');    
        other_option.textContent = `${classroom_data[i].design}`;
        other_option.setAttribute(`value`, `${classroom_data[i].design}`);
        our_element.appendChild(other_option);
    }
    })
  .catch(err => console.log(err))
}





// To create the fields of periods, so the user can fill them :______________________
function generate_inputs(nbr_group, type){
  
  var con_fields = document.getElementById('creates');
  var niv = document.getElementById("level").value;
  //console.log("from create fields function")

  for (var i = 0; i < nbr_group; i++) {
    var div = document.createElement('div');
    div.className = 'removable border m-2 p-2'
    if (type==="TD-TP"){                  
      // create Elements part:=============================
        // type of group part:
      var subDivY = document.createElement('div');
      subDivY.className = 'form-group';
      subDivY.innerHTML = `
      <label class="col-form-label pl-2">type de groupe</label>
      <select class="period-select float-right mr-5 custom-select" style="width: 130px">
        <option disabled selected>--Select--</option>
        <option>TP</option>
        <option>TD</option>
      </select>
      `;
      div.appendChild(subDivY);

        // for group part:
      var subDiv = document.createElement('div');
      var labelSelectG = document.createElement('label');
      var selectElementG = document.createElement('select');
      var first_option_elementG = document.createElement('option');

      first_option_elementG.textContent = "--Select--";
      first_option_elementG.selected = true;
      first_option_elementG.disabled = true;
      selectElementG.appendChild(first_option_elementG);

      for (var s=1; s<=nbr_group; s++) {
        var optionElement = document.createElement('option');
        optionElement.setAttribute(`value`, `G${s}`);        
        optionElement.textContent = `G${s}`;
        selectElementG.appendChild(optionElement);
      }
      labelSelectG.textContent = "groupe";
      
      subDiv.className = 'form-group';
      labelSelectG.className = 'col-form-label pl-2';
      selectElementG.className = 'period-select float-right mr-5 custom-select';
      selectElementG.setAttribute("style", "width: 130px");
      subDiv.appendChild(labelSelectG);
      subDiv.appendChild(selectElementG);
      div.appendChild(subDiv);
      
      // for module part:------------------------------
      var subDivM = document.createElement('div');
      var labelSelectM = document.createElement('label');
      var selectElementM = document.createElement('select');
      var first_option_elementM = document.createElement('option');

      subDivM.className = 'form-group';
      labelSelectM.className = 'col-form-label pl-2';
      labelSelectM.textContent = "Module";
      first_option_elementM.textContent = "--Please select--";
      first_option_elementM.selected = true;
      first_option_elementM.disabled = true;
      selectElementM.className = 'period-select float-right mr-5 custom-select';
      selectElementM.setAttribute("style", "width: 230px");
      selectElementM.value = "";

      module_api(selectElementM, first_option_elementM);

      subDivM.appendChild(labelSelectM);
      subDivM.appendChild(selectElementM);
      div.appendChild(subDivM);
      
      // for teacher part:------------------------------
      var subDivT = document.createElement('div');
      var labelSelectT = document.createElement('label');
      var selectElementT = document.createElement('select');
      var first_option_elementT = document.createElement('option')

      subDivT.className = 'form-group';
      labelSelectT.className = 'col-form-label pl-2';
      labelSelectT.textContent = "Enseignant";
      first_option_elementT.textContent = "--Please select--";
      first_option_elementT.selected = true;
      first_option_elementT.disabled = true;
      selectElementT.className = 'period-select float-right mr-5 custom-select';
      selectElementT.setAttribute("style", "width: 230px");
      selectElementT.value = "";

      
      teacher_api(selectElementT, first_option_elementT);


      subDivT.appendChild(labelSelectT);
      subDivT.appendChild(selectElementT);
      div.appendChild(subDivT);
      
      
      // for classroom part:---------------------------
      var subDivC = document.createElement('div');
      var labelSelectC = document.createElement('label');
      var selectElementC = document.createElement('select');
      var first_option_elementC = document.createElement('option');

      subDivC.className = 'form-group';
      labelSelectC.className = 'col-form-label pl-2';
      labelSelectC.textContent = "Salle";
      first_option_elementC.textContent = "--Please select--";
      first_option_elementC.selected = true;
      first_option_elementC.disabled = true;
      selectElementC.className = 'period-select float-right mr-5 custom-select';
      selectElementC.setAttribute("style", "width: 230px");
      selectElementC.value = "";
      
      classroom_api(selectElementC, first_option_elementC);

      subDivC.appendChild(labelSelectC);      
      subDivC.appendChild(selectElementC); 
      div.appendChild(subDivC);

    //IF the user choosed "COURS" instead of "TD-TP"  
    }else if(type==="Cours"){


      // for module part:------------------------------
      var subDivM = document.createElement('div');
      var labelSelectM = document.createElement('label');
      var selectElementM = document.createElement('select');
      var first_option_elementM = document.createElement('option');

      subDivM.className = 'form-group';
      labelSelectM.className = 'col-form-label pl-2';
      labelSelectM.textContent = "Module";
      first_option_elementM.textContent = "--Please select--";
      first_option_elementM.selected = true;
      first_option_elementM.disabled = true;
      selectElementM.className = 'period-select float-right mr-5 custom-select';
      selectElementM.setAttribute("style", "width: 230px");
      
      module_api(selectElementM, first_option_elementM);

      subDivM.appendChild(labelSelectM);
      subDivM.appendChild(selectElementM);
      div.appendChild(subDivM);
      
      // for teacher part:------------------------------
      var subDivT = document.createElement('div');
      var labelSelectT = document.createElement('label');
      var selectElementT = document.createElement('select');
      var first_option_elementT = document.createElement('option');

      subDivT.className = 'form-group';
      labelSelectT.className = 'col-form-label pl-2';
      labelSelectT.textContent = "Enseignant";
      first_option_elementT.textContent = "--Please select--";
      first_option_elementT.selected = true;
      first_option_elementT.disabled = true;
      selectElementT.className = 'period-select float-right mr-5 custom-select';
      selectElementT.setAttribute("style", "width: 230px");

      teacher_api(selectElementT, first_option_elementT);

      subDivT.appendChild(labelSelectT);
      subDivT.appendChild(selectElementT);
      div.appendChild(subDivT);
      
      
      // for classroom part:---------------------------
      var subDivC = document.createElement('div');
      var labelSelectC = document.createElement('label');
      var selectElementC = document.createElement('select');
      var first_option_elementC = document.createElement('option');


      subDivC.className = 'form-group';
      labelSelectC.className = 'col-form-label pl-2';
      labelSelectC.textContent = "Salle";
      first_option_elementC.textContent = "--Please select--";
      first_option_elementC.selected = true;
      first_option_elementC.disabled = true;
      selectElementC.className = 'period-select float-right mr-5 custom-select';
      selectElementC.setAttribute("style", "width: 230px");

      classroom_api(selectElementC, first_option_elementC);

      subDivC.appendChild(labelSelectC);      
      subDivC.appendChild(selectElementC); 
      div.appendChild(subDivC);
    }
    con_fields.insertBefore(div, con_fields.childNodes[0]);
  }
}



// This function verify all the data of the table and compares it with canvas:_____________
var verify_modules_periods = async (periodType, user_input) => {
  let forceEnable = false;
  await fetch('http://127.0.0.1:8000/api/module-list')
  .then(res =>  res.json())
  .then((canvas_data) => {

    if(periodType === "TP") {
      for (let i = 0; i < canvas_data.length; i++) {
        if (canvas_data[i].designation === user_input.value){
          
          if (`${user_input.value}` in counters_module_TP === false && user_input.getAttribute("data-previous-value") === "") {
            counters_module_TP[`${user_input.value}`] = 1;

          }else if(`${user_input.value}` in counters_module_TP === false && user_input.getAttribute("data-previous-value") !== "") {
            counters_module_TP[`${user_input.value}`] = 1;
            counters_module_TP[`${user_input.getAttribute("data-previous-value")}`] -= 1;

          }else if (counters_module_TP[`${user_input.value}`] >= canvas_data[i].tp) {
            let modalHeader = document.querySelector(".modal-header");
            const div = document.createElement('div');
            const textNode = document.createTextNode(`canvas tells that this module (${user_input.value}) has just ${canvas_data[i].tp} TP per timetable`);
            div.className = "alert alert-danger ml-4 mr-4 ";
            div.appendChild(textNode);
            modalHeader.insertBefore(div, modalHeader.childNodes[2]);
            
            // after 2s the alert message will be deleted (fade in animation)
            setTimeout(()=>{
              let ambiguity = 1;
              let setintervalID = setInterval(fadeIn, 50);
              function fadeIn () {
                if (ambiguity > 0){
                  ambiguity = ambiguity - 0.1;
                  div.style.opacity = ambiguity;
                } else {
                  clearInterval(setintervalID);
                  modalHeader.removeChild(modalHeader.childNodes[2]);
                }
              }
            }, 3000);
            forceEnable = true;
          }else if (user_input.getAttribute("data-previous-value") === "") {
            counters_module_TP[`${user_input.value}`] += 1;
          }else {
            counters_module_TP[`${user_input.value}`] += 1;
            counters_module_TP[`${user_input.getAttribute("data-previous-value")}`] -= 1;
          }

        }
      }
    }else if (periodType === "TD") {
      for (let i = 0; i < canvas_data.length; i++) {
        if (canvas_data[i].designation === user_input.value){
          
          if (`${user_input.value}` in counters_module_TD === false && user_input.getAttribute("data-previous-value") === "") {
            counters_module_TD[`${user_input.value}`] = 1;

          }else if(`${user_input.value}` in counters_module_TD === false && user_input.getAttribute("data-previous-value") !== "") {
            counters_module_TD[`${user_input.value}`] = 1;
            counters_module_TD[`${user_input.getAttribute("data-previous-value")}`] -= 1;

          }else if (counters_module_TD[`${user_input.value}`] >= canvas_data[i].td) {
            let modalHeader = document.querySelector(".modal-header");
            const div = document.createElement('div');
            const textNode = document.createTextNode(`canvas tells that this module (${user_input.value}) has just ${canvas_data[i].td} TP per timetable`);
            div.className = "alert alert-danger ml-4 mr-4 ";
            div.appendChild(textNode);
            modalHeader.insertBefore(div, modalHeader.childNodes[2]);
            
            // after 2s the alert message will be deleted (fade in animation)
            setTimeout(()=>{
              let ambiguity = 1;
              let setintervalID = setInterval(fadeIn, 50);
              function fadeIn () {
                if (ambiguity > 0){
                  ambiguity = ambiguity - 0.1;
                  div.style.opacity = ambiguity;
                } else {
                  clearInterval(setintervalID);
                  modalHeader.removeChild(modalHeader.childNodes[2]);
                }
              }
            }, 3000);
            forceEnable = true;
          }else if (user_input.getAttribute("data-previous-value") === "") {
            counters_module_TD[`${user_input.value}`] += 1;
          }else {
            counters_module_TD[`${user_input.value}`] += 1;
            counters_module_TD[`${user_input.getAttribute("data-previous-value")}`] -= 1;  
          }

        }
      }
    }else if(periodType === "Cours"){
      for (let i = 0; i < canvas_data.length; i++) {
        if (canvas_data[i].designation === user_input.value){
          
          if (`${user_input.value}` in counters_module_Cours === false && user_input.getAttribute("data-previous-value") === "") {
            counters_module_Cours[`${user_input.value}`] = 1;

          }else if(`${user_input.value}` in counters_module_Cours === false && user_input.getAttribute("data-previous-value") !== "") {
            counters_module_Cours[`${user_input.value}`] = 1;
            counters_module_Cours[`${user_input.getAttribute("data-previous-value")}`] -= 1;

          }else if (counters_module_Cours[`${user_input.value}`] >= canvas_data[i].cours) {
            let modalHeader = document.querySelector(".modal-header");
            const div = document.createElement('div');
            const textNode = document.createTextNode(`canvas tells that this module (${user_input.value}) has just ${canvas_data[i].cours} cours per timetable`);
            div.className = "alert alert-danger ml-4 mr-4 ";
            div.appendChild(textNode);
            modalHeader.insertBefore(div, modalHeader.childNodes[2]);
            
            // after 2s the alert message will be deleted (fade in animation)
            setTimeout(()=>{
              let ambiguity = 1;
              let setintervalID = setInterval(fadeIn, 50);
              function fadeIn () {
                if (ambiguity > 0){
                  ambiguity = ambiguity - 0.1;
                  div.style.opacity = ambiguity;
                } else {
                  clearInterval(setintervalID);
                  modalHeader.removeChild(modalHeader.childNodes[2]);
                }
              }
            }, 3000);
            forceEnable = true;
          }else if (user_input.getAttribute("data-previous-value") === "") {
            counters_module_Cours[`${user_input.value}`] += 1;
          }else {
            counters_module_Cours[`${user_input.value}`] += 1;
            counters_module_Cours[`${user_input.getAttribute("data-previous-value")}`] -= 1;
          }

        }
      }
    }

  }).catch(err => console.log("from catch promise", err))
  return forceEnable;
}






// This function checks if an input of the user was empty or not
function check_empty_input() {
  console.log("check empty inputs function")
  let user_inputs = document.querySelectorAll(".period-select")
  let empty_input = false

  user_inputs.forEach((input)=> {
    if (input.value === "--Select--" || input.value === "--Please select--") {
      input.style.border = "1px solid red";
      empty_input = true
    } 
  })

  if(empty_input){
    let modalHeader = document.querySelector(".modal-header");
    const div = document.createElement('div');
    const textNode = document.createTextNode("all fields are required !!!");
    div.className = "alert alert-danger ml-4 mr-4 ";
    div.appendChild(textNode);
    modalHeader.insertBefore(div, modalHeader.childNodes[2]);
    
      // after 2s the alert message will be deleted (fade in animation)
      setTimeout(()=>{
      let ambiguity = 1;
      let setintervalID = setInterval(fadeIn, 50);
      function fadeIn () {
        if (ambiguity > 0){
          ambiguity = ambiguity - 0.1;
          div.style.opacity = ambiguity;
        } else {
          clearInterval(setintervalID);
          modalHeader.removeChild(modalHeader.childNodes[2]);
        }
      }
    }, 3000);
  } 
  return empty_input
}
// This function checks the inputs of user IF he selected a given input before or not :___________________________
function examine_inputs(callbackFunction, periodType) {
  var user_inputs = document.querySelectorAll(".period-select")

  if (periodType === "TD-TP") {
    for (let e = 0; e < user_inputs.length; e++) {
      user_inputs[e].setAttribute("data-previous-value", `${user_inputs[e].value}`);
      user_inputs[e].addEventListener('change', (event) => {
        
        if (user_inputs[e].previousSibling.textContent === "groupe") {
          let dataG_attr = user_inputs[e].getAttribute("data-previous-value");
          let childG;
            // this condition is for the user if change his choise or not, if so, 
            // the next lines will change his choise to the new one
          if (user_inputs[e].getAttribute("data-previous-value") === "--Select--") {
            var g = 0;
            for (let i = 1; i < user_inputs.length; i++) {
              if(g%5 === 0) {
                childG = searchIn_select(user_inputs[i], user_inputs[e].value);
                childG.disabled = true;
                childG.style.backgroundColor = "#d9d3d3";
              }
              g = g+1;
            }
          }else {
            //this loop takes the user's input value and disable the other
            //input options in the next inputs that equates that value
            for (let i = 1; i < user_inputs.length; i++) {
              if(g%5 === 0) {
                childG = searchIn_select(user_inputs[i], user_inputs[e].value);
                childG.disabled = true;
                childG.style.backgroundColor = "#d9d3d3";
                let changed_value = searchIn_select(user_inputs[i], dataG_attr);
                changed_value.disabled = false;
                changed_value.style.backgroundColor = "";
              }
              g = g+1;
            }
          }
          user_inputs[e].setAttribute("data-previous-value", `${user_inputs[e].value}`);


        // if the user is standing on a "Module" input
        } else if (user_inputs[e].previousSibling.textContent === "Module"){
          callbackFunction(user_inputs[e-2].value, user_inputs[e])
          .then(forceEnable => {
            let m = 0;

            let dataM_attr = user_inputs[e].getAttribute("data-previous-value");
            
            if (user_inputs[e].getAttribute("data-previous-value") === "" && !forceEnable) {
              
              for (let i = 2; i < user_inputs.length; i++) {
                if(m%5 === 0) {
                  let childM = searchIn_select(user_inputs[i], user_inputs[e].value);
                  childM.disabled = true;
                  childM.style.backgroundColor = "#d9d3d3";
                }
                m = m+1;
              }
              user_inputs[e].setAttribute("data-previous-value", `${user_inputs[e].value}`);
            }else if (!forceEnable) {
              
              for (let i = 2; i < user_inputs.length; i++) {
                if(m%5 === 0) {
                  let childM = searchIn_select(user_inputs[i], user_inputs[e].value);
                  childM.disabled = true;
                  childM.style.backgroundColor = "#d9d3d3";
                  let changed_value = searchIn_select(user_inputs[i], dataM_attr);
                  changed_value.disabled = false;
                  changed_value.style.backgroundColor = "";
                }
                m = m+1;
              }
              user_inputs[e].setAttribute("data-previous-value", `${user_inputs[e].value}`);
            }else if (user_inputs[e].getAttribute("data-previous-value") !== "" && forceEnable) {
              setTimeout(() => {
                let childM = searchIn_select(user_inputs[e], user_inputs[e].value);
                let pre_option = searchIn_select(user_inputs[e], user_inputs[e].getAttribute("data-previous-value"));
                childM.disabled = false;
                childM.style.backgroundColor = "";
                pre_option.selected = true;
                user_inputs[e].setAttribute("data-previous-value", `${user_inputs[e].value}`);
              }, 3000);

            }else {
              
              setTimeout(() => {
                let childM = searchIn_select(user_inputs[e], user_inputs[e].value);
                let def_option = searchIn_select(user_inputs[e], "--Please select--");
                childM.disabled = false;
                childM.style.backgroundColor = "";
                def_option.selected = true;
                user_inputs[e].setAttribute("data-previous-value", `${user_inputs[e].value}`);
              }, 3000);
            }
          })
          .catch(err => console.log(err))
        
        // if the user is standing on a "Teacher" input
        }else if (user_inputs[e].previousSibling.textContent === "Enseignant") {
          let t = 0;
          let childE;
          let dataT_attr = user_inputs[e].getAttribute("data-previous-value");

          if (user_inputs[e].getAttribute("data-previous-value") === "") {
            for (let i = 3; i < user_inputs.length; i++) {
              if(t%5 === 0) {
                childE = searchIn_select(user_inputs[i], user_inputs[e].value);
                childE.disabled = true;
                childE.style.backgroundColor = "#d9d3d3";
              }
              t = t+1;
            }
          }else {
            for (let i = 3; i < user_inputs.length; i++) {
              if(t%5 === 0) {
                childE = searchIn_select(user_inputs[i], user_inputs[e].value);
                childE.disabled = true;
                childE.style.backgroundColor = "#d9d3d3";
                let changed_value = searchIn_select(user_inputs[i], dataT_attr);
                changed_value.disabled = false;
                changed_value.style.backgroundColor = "";
              }
              t = t+1;
            }
          }
          user_inputs[e].setAttribute("data-previous-value", `${user_inputs[e].value}`);

        // if the user is standing on a "Classroom" input
        }else if (user_inputs[e].previousSibling.textContent === "Salle") {
          let c = 0;
          let childC;
          let dataC_attr = user_inputs[e].getAttribute("data-previous-value");


          if (user_inputs[e].getAttribute('data-previous-value') === "") {
            for (let i = 4; i < user_inputs.length; i++) {
              if(c%5 === 0) {
                childC = searchIn_select(user_inputs[i], user_inputs[e].value);
                childC.disabled = true;
                childC.style.backgroundColor = "#d9d3d3";
              }
              c = c+1;
            }
          } else {
            for (let i = 4; i < user_inputs.length; i++) {
              if(c%5 === 0) {
                childC = searchIn_select(user_inputs[i], user_inputs[e].value);
                childC.disabled = true;
                childC.style.backgroundColor = "#d9d3d3";
                let changed_value = searchIn_select(user_inputs[i], dataC_attr);
                changed_value.disabled = false;
                changed_value.style.backgroundColor = "";
              }
              c = c+1;
            }
          }
          user_inputs[e].setAttribute("data-previous-value", `${user_inputs[e].value}`);

        }
      });
    }
  }else if(periodType === "Cours") {
      user_inputs[0].setAttribute("data-previous-value", `${user_inputs[0].value}`);
      user_inputs[0].addEventListener('change', (event) => {
        if (user_inputs[0].previousSibling.textContent === "Module"){
          callbackFunction("Cours", user_inputs[0])
          .then((forceEnable)=>{

            if (user_inputs[0].getAttribute("data-previous-value") !== "" && forceEnable) {
              setTimeout(() => {

                let pre_option = searchIn_select(user_inputs[0], user_inputs[0].getAttribute("data-previous-value"));
                pre_option.selected = true;
                user_inputs[0].setAttribute("data-previous-value", `${user_inputs[0].value}`);
              }, 3000);

            }else if (forceEnable) {
              setTimeout(() => {
                let def_option = searchIn_select(user_inputs[0], "--Please select--");
                def_option.selected = true;
                user_inputs[0].setAttribute("data-previous-value", `${user_inputs[0].value}`);
              }, 3000);
            }else{
              user_inputs[0].setAttribute("data-previous-value", `${user_inputs[0].value}`);
            }

          })
          .catch((err)=>{
            console.log("error", err)
          })
        }
      })
    
  }
}




// This function insert the values of fields into the period content:__________________________
function insertPeriodT(nbr_group, event, id, our_object, type_of_period){
  var formChild = ""; 
  var groupe, br, j;
  var inputlist = [];
  var singleInput = document.querySelectorAll('.period-select')

  our_object[`${id}`] = {};
  our_object[`${id}`]['type'] = type_of_period;
  for (var i = 0; i < nbr_group*5; i++){ 
    j= i+1;

    if (i%5 === 0){ 
      groupe = document.createElement('span');
      br = document.createElement('br');
      groupe.classList = 'existed style-block'; 
    }       
    
    formChild = document.querySelectorAll('.period-select')[i].value;
    groupe.textContent = groupe.textContent + " " + formChild;
    inputlist[i%5] = formChild;

    if (j%5 === 0){
      our_object[`${id}`][`${j%nbr_group}`] = {type_of_group: inputlist[0], groupe: inputlist[1], module: inputlist[2], enseignant: inputlist[3], salle: inputlist[4]};
      event.appendChild(groupe);
      event.appendChild(br);
      event.classList.add('existed');
      inputlist = [];
    }
  }
  resetInputs();
}
// This function insert the values of fields into the...
//period content when the selected input is COURS:___________________________________
function insertPeriodC(event, id, our_object, type_of_period) {
  var inputlist = [],
      col, formInputs;

  for(var i=0; i<3; i++){
    col = document.createElement('div');
    formInputs = document.querySelectorAll('.period-select')[i].value;
    inputlist[i] = formInputs;
    col.appendChild(document.createTextNode(formInputs));
    col.className = 'our_col existed';
    event.appendChild(col);
  }
  
  event.classList.add('existed');

  our_object[`${id}`] = {module: inputlist[0], enseignant: inputlist[1], salle: inputlist[2], type: type_of_period};
  resetInputs();
}



// when the user click on any period from the table:=========================================
function period_tb_click(event) {   
    event.preventDefault()  
    event.stopPropagation()  
    event_period = event.target;
    id_event = event.target.id;
    
    var level_table = document.getElementById("level")
    var nbr_group = document.getElementById("nbr-group")
    var semester = document.getElementById("semestre")
    var click_counter = 0
    if (level_table.value === "" || nbr_group.value === "" || semester.value === "") {
      alert("you need to select the level of the table and the number of groups and the semester before filling the table !!")
      return 
    }
    
    $('#exampleModall').modal('show');
    event.target.innerHTML= "";
    
    
    $("#closes").click(function () {
      $('#exampleModall').modal('hide');
    });
        
}
// when the user choose either TP/TD or Cours:
function td_cr_click(ev) {
  // When the user select 'cours' or 'TD/TP'________________________________________________    
   
  
    const choise = document.getElementById("select-TD-cours");
    const nmb_group = document.querySelector("#group-numb-input");

      if (choise.value === 'TD-TP') {        
        
        // initializing...
        nmb_group.textContent = parseInt(document.getElementById("nbr-group").value);
        document.querySelector(".hidden-part").hidden = false
        document.querySelector(".row.pb").hidden = true
        
        // COUR---------------------------------------COUR---------------------------------------COUR
      }else if(choise.value === 'Cours') {

        // if(cours_was_submitted) {
        //   console.log("before returning function")
        //   return
        // }

        let nbr_group = 1;
        generate_inputs(nbr_group, choise.value); 

        const user_input_values = document.querySelectorAll(".period-select");

        // checking the user's input if any was empty
        user_input_values.forEach(input=>{
          input.addEventListener("change", ()=>{

            if(input.value !== "--Select--" && input.value !== "--Please select--" && input.style.border === "1px solid red"){
              input.style.border = "";
            }
              
          })
        })

        // checking the user's inputs _____________________
        examine_inputs(verify_modules_periods, choise.value);
        
        // if the user clicked to generate inputs this will prevent his to click again
        cours_was_submitted = true
        
      }
      ev.preventDefault(); 
  
}
// generating inputs for the user so he can fill them
function nbr_group_click() {

  // if (tdp_was_submitted) {
  //   console.log("before returning function 'nbr group' ")
  //   return
  // }

  const choise = document.getElementById("select-TD-cours");
  const nmb_group = document.querySelector("#group-numb-input")
  
  generate_inputs(parseInt(nmb_group.textContent), choise.value);

  const user_input_values = document.querySelectorAll(".period-select");

  // checking the user's input if any was empty
  user_input_values.forEach(input=>{
    input.addEventListener("change", ()=>{
      
      if(input.value !== "--Select--" && input.value !== "--Please select--" && input.style.border === "1px solid red"){
        input.style.border = "";
      }
        
    })
  })


  //calling this function to check user inputs if they are frequent:  
  examine_inputs(verify_modules_periods, choise.value);

  // if the user clicked to generate inputs this will prevent his to click again
  tdp_was_submitted = true
}

$('#close').on('click', function(){
  
  $('#exampleModall').modal('hide');
  });


              
// Ajax function for sending the data to the server  _______________________-::-_______________________

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




function sendData(e){

  console.log(dataObject)

  let count = 0

    for(var key in dataObject){
      if(key in dataObject) {
        count++
      }
    }
    console.log("number of periods are : ", count)


  if (JSON.stringify(dataObject) == "{}" || count < 3) {
    alert("you have to fill the table with 3 periods at least !!")
    return
  }



  // fetch("saveData/", {
  //   methed: "POST",
  //   headers: {
  //     "Content-Type": "application/json",
  //     "X-CSRFToken": getCookie("csrftoken")
  //   },
  //   body: JSON.stringify({
  //     "level" : document.getElementById("level").value,
  //     "semestre": document.getElementById("semestre").value,
  //     "our_data" : JSON.stringify(dataObject)
  //   }),
  // })
  // .then(res => {
  //   if(res.ok){
  //     console.log("the data was received seccessfuly to the server side")
  //     window.location.href = 'http://127.0.0.1:8000/dashboard/all-timetables/'
  //   }else {
  //     console.log("the data didn't received to the server side !!!", res)
  //   }
  //   // this return another promise that it will be resolved in the next then()
  //   return res.json()
  // })
  // .then(data => console.log("the returned data : ", data))

 
 
 
 
  $.ajax({
    method: "POST",
    url: "saveData/",
    headers: { "X-CSRFToken": getCookie("csrftoken") },
    data: {
      "level" : document.getElementById("level").value,
      "semestre": document.getElementById("semestre").value,
      "our_data" : JSON.stringify(dataObject),
    },
    //dataType: json,
    success: function(json){
      console.log(json.successMsg);
      console.log("the data receiced to the database");
      var inputs = document.querySelectorAll('.period-select').value;
      for(var i=0; i< 3; i++) {
        console.log(i);
        console.log(inputs);
      }

      window.location.href = 'http://127.0.0.1:8000/dashboard/all-timetables/'
    },
    error: function(errmsg){
      console.log(errmsg);
      console.log("the data didn't received to the database");
    }
  });
}  




  
 


              
 






