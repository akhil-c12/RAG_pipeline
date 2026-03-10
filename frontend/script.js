const API = "http://localhost:5000";

async function uploadPDF(){

const fileInput = document.getElementById("pdfFile");
const file = fileInput.files[0];

if(!file){
alert("Please select a PDF");
return;
}

const formData = new FormData();
formData.append("file", file);

const res = await fetch(API + "/upload",{
method:"POST",
body:formData
});

const data = await res.json();

document.getElementById("uploadStatus").innerText = JSON.stringify(data,null,2);

loadDocuments();

}

async function sendQuery(){

const query = document.getElementById("queryInput").value;

if(!query){
alert("Enter a question");
return;
}

const res = await fetch(API + "/chat",{

method:"POST",
headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
query:query
})

});

const data = await res.json();

document.getElementById("responseBox").innerText = data.answer || data.error;

}

async function loadDocuments(){

const res = await fetch(API + "/documents");

const data = await res.json();

const list = document.getElementById("docList");

list.innerHTML="";

data.documents.forEach(doc=>{

const li=document.createElement("li");

li.innerText=doc;

list.appendChild(li);

});

}