const targets = document.querySelectorAll(".our_target");
const timetable_id = document.querySelector(".our_table").getAttribute("data-timetable-id");
const btn_cancel_modf = document.querySelector(".btn-cancel-modification")
const btn_confirm_modf = document.querySelector(".btn-confirm-modification")






const id_period_converter = {
    1: 'first_first',
    2: 'first_second',
    3: 'first_third',
    4: 'first_forth',
    5: 'second_first',
    6: 'second_second',
    7: 'second_third',
    8: 'second_forth',
    9: 'third_first',
    10: 'third_second',
    11: 'third_third',
    12: 'third_forth',
    13: 'forth_first',
    14: 'forth_second',
    15: 'forth_third',
    16: 'forth_forth',
    17: 'fifth_first',
    18: 'fifth_second',
    19: 'fifth_third',
    20: 'fifth_forth',

}

targets.forEach(target => {target.addEventListener("click", period_tb_click)});
btn_cancel_modf.addEventListener("click", cancel_modf)
btn_confirm_modf.addEventListener("click", confirm_modf)




function cancel_modf() {
    $('#exampleModall').modal('hide');
}


function confirm_modf() {
    const confirmation = document.querySelector(".confirmation")
    const select_tp_cours = document.querySelector(".row.pb")

    confirmation.hidden = true
    select_tp_cours.hidden = false
}

function timetable_api(){
    const url = `http://127.0.0.1:8000/api/timetable-detail/${timetable_id}`
    console.log("our timetable url is: ", url)
    fetch(url)
    .then(res =>{
        if(res.ok) {
            console.log("success")
        }else {
            console.log("error , something went wrong")
        }
        return res.json()
    })
    .then(data =>{
        console.log("data api: ", data)
    })
}



function module_api() {
    const url = "http://127.0.0.1:8000/api/module-list"


    fetch(url)
    .then(res =>{
        if(res.ok) {
            console.log("success")
        }else {
            console.log("error , something went wrong")
        }
        return res.json()
    })
    .then(data =>{
        console.log("MODULE data api: ", data)

        console.log('length is :', data.length)

        data.forEach((module)=>{
            console.log("nom de module : ", module.tp)
        })
    })


}









function period_tb_click (ev){
    e = ev.target.id
    console.log("this is the id of period", e);
    timetable_api()


    console.log("module api: ", module_api())

    $('#exampleModall').modal('show');
}













$('#close').on('click', function(){
  
    $('#exampleModall').modal('hide');
    });
  
  