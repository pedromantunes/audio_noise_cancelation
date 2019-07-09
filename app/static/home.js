let step = 'step1';

const step1 = document.getElementById('step1');
const step2 = document.getElementById('step2');
const step3 = document.getElementById('step3');
const step4 = document.getElementById('step4');

function next(phase) {
  if (phase === 'initial') {
    step = 'step2';
    step1.classList.remove("is-active");
    step1.classList.add("is-complete");
    step2.classList.add("is-active");

  } else if (phase === 'audio_extracted') {
    step = 'step3';
    step1.classList.remove("is-active");
    step1.classList.add("is-complete");
    step2.classList.add("is-active");
    step2.classList.remove("is-active");
    step2.classList.add("is-complete");
    step3.classList.add("is-active");

  } else if (phase === 'silence_segments') {
    step = 'step4';
    step1.classList.remove("is-active");
    step1.classList.add("is-complete");
    step2.classList.add("is-active");
    step2.classList.remove("is-active");
    step2.classList.add("is-complete");
    step3.classList.add("is-active");
    step3.classList.remove("is-active");
    step3.classList.add("is-complete");
    step4.classList.add("is-active");

  } else if (phase === 'silence_removed') {
    step = 'complete';
    step1.classList.remove("is-active");
    step1.classList.add("is-complete");
    step2.classList.add("is-active");
    step2.classList.remove("is-active");
    step2.classList.add("is-complete");
    step3.classList.add("is-active");
    step3.classList.remove("is-active");
    step3.classList.add("is-complete");
    step4.classList.add("is-active");
    step4.classList.remove("is-active");
    step4.classList.add("is-complete");

  } else if (phase === 'complete') {
    step = 'step1';

    step4.classList.remove("is-complete");
    step3.classList.remove("is-complete");
    step2.classList.remove("is-complete");
    step1.classList.remove("is-complete");
    step1.classList.add("is-active");
  }
}

var theForm = document.forms['file_form']
var token = ""


function addHidden(theForm, key, value) {
    // Create a hidden input element, and append it to the form:
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = key; // 'the key/name of the attribute/field that is sent to the server
    input.value = value;
    theForm.appendChild(input);
}


const Http = new XMLHttpRequest();
const url='http://localhost:5001/get_id';
Http.open("GET", url);
Http.send();

Http.onreadystatechange = (e) => {
    if(XMLHttpRequest.DONE && Http.readyState==4)
    {
        token = Http.responseText;
        addHidden(theForm, 'token', Http.responseText);
    }
}



function checkUpdates(url) {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url);
  xhr.onreadystatechange = (e) => {
    if(XMLHttpRequest.DONE && Http.readyState==4)
    {
        console.log(xhr.responseText)
        if(xhr.responseText !== "")
        {
            next(JSON.parse(xhr.responseText))
        }
    }
}
  xhr.send();
}

setInterval(function() { checkUpdates('http://localhost:5001/get_status?id=' + token) }, 5000);


