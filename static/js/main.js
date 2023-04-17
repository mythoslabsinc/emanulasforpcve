function autoHeight(obj) { // add auto enlarging box
    obj.style.height = 0;
    obj.style.setProperty("height",(obj.scrollHeight) + "px", "important");
  }
function resizeTextbox() { // add auto enlarging box
  this.style.height = 0;
  this.style.setProperty("height",(this.scrollHeight) + "px", "important");
}

function tickanimation(obj){
  obj.classList.add("fa-check");
  obj.style.setProperty("background", "green");
    setTimeout( function(){
      obj.classList.remove("fa-check");
      obj.style.setProperty("background", "#1c1d1d");
  },300);

  
}

function copyOutput(id){
  var copyText = document.getElementById(id);
  // // Select the text field
  // copyText.select();
  // copyText.setSelectionRange(0, 99999); // For mobile devices
  // Copy the text inside the text field
  navigator.clipboard.writeText(copyText.value);
}
  
// For Processing
  function getNextOutput(count, delay, formJSON){
    if(count <= 0) {
        // show the generate button again
        document.getElementById("theLoadingAnimation").style.display="none";
        document.getElementById("theSubmitButton").style.display="flex";
        return;
    }
    var xhr = new XMLHttpRequest();
    var url = "/template-query";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);
            var outputText = json.output;
            outputText = outputText.trim();
            var outputFormat = json.outputFormat;
            var query = json.query;
            document.getElementById("theQuery").innerHTML = query;
            showNextOutput(count, delay, formJSON, outputText, outputFormat);
        }
    };
    //var data = JSON.stringify({"query": query});
    var data = JSON.stringify(formJSON)
    xhr.send(data);
  };
  
  function showNextOutput(count, delay,formJSON, outputText, outputFormat){
    if(count <= 1) delay = 0;
    theOutputsList = document.getElementById("theOutputsList")
    // Now I have to show this output over there
    var block = `
    <div class="row" >
      <div class="col-sm-9 mx-auto">
        <div class="card card-signin out-block">
          <div class="card-body card-center img-top-card">
            <img src = "../static/images/${outputFormat}_t.png" class="img-fluid w-100"/>
          </div>
          <textarea class = "outputText" id="o${count}" onfocusout='disableEdit(${count})'
              placeholder = " " oninput="autoHeight(this)" {reqtext} readonly>${outputText}</textarea>
          <div class="card-body card-center img-bottom-card">
            <img src = "../static/images/${outputFormat}_b.png" class="img-fluid w-100"/>
          </div>
        </div>
        <div class="buttonbox">
          <i class="fa fa-pencil iconbutton iconbutton0" id="e${count}" onclick="toggleEdit('o${count}'); toggleClick(this)" aria-hidden="true"></i>
          <i class="fa fa-download iconbutton iconbutton1" id="d${count}" onclick="saveText('o${count}');tickanimation(this)" aria-hidden="true"></i>
          <i class="fa fa-copy iconbutton iconbutton2" id="c${count}" onclick="copyOutput('o${count}');tickanimation(this)" aria-hidden="true"></i>
        </div>
      </div>
    </div>
    `
    theOutputsList.innerHTML =  theOutputsList.innerHTML + block;
    autoHeight(document.getElementById("o"+count))
    setTimeout(() => {
    getNextOutput(count-1,delay,formJSON);
    }, delay);
  };
  
  function handleFormSubmit(event) {
    event.preventDefault();
    const data = new FormData(event.target);
    const formJSON = Object.fromEntries(data.entries());
    // for multi-selects, we need special handling
    // but since there aren't any multitexts yet, we dont need it
    //formJSON.snacks = data.getAll('snacks');
    
    // hide the generate button
    document.getElementById("theSubmitButton").style.display="none";
    document.getElementById("theLoadingAnimation").style.display="flex"
    // first clean the outputs present
    document.getElementById("theOutputsList").innerHTML='';
    // get count and delay
    var count= document.getElementById("theOutputCount").value;
    var delay= document.getElementById("theOutputDelay").value;
    if(count == "") count = 1
    if(delay == "") delay = 0
    delay *= 1000
    
    getNextOutput(count, delay, formJSON);
    
  }

// For icons
function toggleEdit(id){
  document.getElementById(id).readOnly = !document.getElementById(id).readOnly;
  document.getElementById(id).classList.toggle('editable');
}

function toggleClick(obj){
  obj.classList.toggle('clicked');
}

function disableEdit(i){
  document.getElementById("o"+i).readOnly = true;
  document.getElementById("o"+i).classList.remove('editable');
  document.getElementById("e"+i).classList.remove('clicked');
}

function downloadText(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

function saveText(id){
  textbox = document.getElementById(id);
  var content = textbox.value;
  var filename = "output.txt";
  downloadText(filename, content);
}

// Running
if ( window.history.replaceState ) {
  window.history.replaceState( null, null, window.location.href );
} // This makes sure that refresh doesnt process the code again


const form = document.getElementById('theMainFormId');
form.addEventListener('submit', handleFormSubmit);

const tx = document.getElementsByTagName("textarea");
for (let i = 0; i < tx.length; i++) {
  tx[i].setAttribute("style", "height:" + (tx[i].scrollHeight) + "px!important;overflow-y:hidden;margin-right:8px!important");
  tx[i].addEventListener("input", resizeTextbox, false);
}