function completeTask(e,el){

e.preventDefault()

fetch(el.href,{method:'PATCH'})
.then(()=>location.reload())

}

function deleteTask(e,el){

e.preventDefault()

fetch(el.href,{method:'DELETE'})
.then(()=>location.reload())

}


function editTask(id,title,description,priority){

let newTitle = prompt("Edit title:",title)
if(newTitle===null) return

let newDesc = prompt("Edit description:",description)
if(newDesc===null) newDesc=""

let newPriority = prompt("Priority (low / medium / high):",priority)
if(newPriority===null) newPriority=priority

fetch(`/api/tasks/${id}`,{
method:"PUT",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
title:newTitle,
description:newDesc,
priority:newPriority
})
}).then(()=>location.reload())

}


function filterTasks(type){

let url="/api/tasks"

if(type==="pending") url+="?completed=false"
if(type==="completed") url+="?completed=true"

fetch(url)
.then(res=>res.json())
.then(renderTasks)

}


function filterPriority(level){

fetch(`/api/tasks?priority=${level}`)
.then(res=>res.json())
.then(renderTasks)

}


function renderTasks(tasks){

const container = document.getElementById("taskList")

container.innerHTML=""

tasks.forEach(task=>{

let dueDate = ""

if(task.due_date){
dueDate = `<p class="due">Due: ${task.due_date.split("T")[0]}</p>`
}

let doneButton = ""

if(!task.completed){
doneButton = `
<a href="/api/tasks/${task.id}"
onclick="completeTask(event,this)">
✓ Done
</a>
`
}

let html = `
<div class="task ${task.completed ? 'done' : ''}">

<div>

<strong>${task.title}</strong>

<p class="desc">${task.description || ""}</p>

<div class="priority ${task.priority}">
${task.priority} Priority
</div>

${dueDate}

</div>

<div class="task-actions">

${doneButton}

<a href="#"
onclick="editTask(${task.id},'${task.title}','${task.description || ""}','${task.priority}')">
✏ Edit
</a>

<a href="/api/tasks/${task.id}"
onclick="deleteTask(event,this)">
🗑 Delete
</a>

</div>

</div>
`

container.innerHTML += html

})

}