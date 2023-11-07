const store = {
  user: {
    "email": "",
    "password": ""
  },
  n: "",
  buttons_counter: 0,
  tasks: {}  
}


async function loginUser() {
  try {
    const response = await fetch("http://127.0.0.1/signin", {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json'  
      },
      body: JSON.stringify(store.user)
    })

    const data = await response.json();
    return data
  }
  catch (error) {
    console.error("Error:", error);
    return 
  }
}

async function registerUser() {
  try {
    const response = await fetch("http://127.0.0.1/register", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(store.user)
    })

    const data = await response.json();
    return data
  }
  catch (error) {
    console.error("Error:", error);
    return 
  }
}

async function getUserData (formId){
  event.preventDefault();
  let info_container_id, modal_id, message;

  if (formId == 'loginForm') {
    store.user.email = document.getElementById('login_username').value;
    store.user.password = document.getElementById('login_password').value;
    info_container_id = 'container__login-info';
    modal_id = 'id01';
    message = "successfully logged in";
  }
  else {
    store.user.email = document.getElementById('register_username').value;
    store.user.password = document.getElementById('register_password').value;
    info_container_id = 'container__register-info';
    modal_id = 'id02';
    message = "successfully registered";
  }


  if (formId == 'loginForm') {
    result = await loginUser();
  }
  else {
    result = await registerUser();
  }



  if (result["ok"]) {
    document.getElementById(info_container_id).innerHTML = message;
    document.getElementById(info_container_id).style.color = "#52BA31";
    setTimeout(() => {
      document.getElementById(info_container_id).innerHTML = "";
      document.getElementById(formId).reset();
      document.getElementById(modal_id).style.display = "none";

      renderHomePage()
    }, 1500);
  }
  else { 
    document.getElementById(info_container_id).innerHTML = result["description"];
    document.getElementById(info_container_id).style.color = "tomato"
  }
  return true;
}

// renderHomePage()

// HomePage
async function createTask() {
  try {
    const response = await fetch("http://127.0.0.1/createTask", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({...store.user, "input_data": store.n})
    })

    const data = await response.json();
    return data
  }
  catch (error) {
    console.error("Error:", error);
    return 
  }
}

async function getTasks() {
  try {
    const response = await fetch("http://127.0.0.1/getTasks", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(store.user)
    })

    const data = await response.json();
    return data
  }
  catch (error) {
    console.error("Error:", error);
    return 
  }
}

async function cancelTask(task_id) {
  try {
    const response = await fetch("http://127.0.0.1/cancelTask", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({...store.user, "task_id": task_id})
    })

    const data = await response.json();
    return data
  }
  catch (error) {
    console.error("Error:", error);
    return 
  }
}

async function getNumber() {
  event.preventDefault();
  store.n = document.getElementById("n_operation").value;
  error_field = document.getElementById("error-field")

  result = await createTask();
  if (result["ok"]) {
    error_field.innerHTML = "";
  }
  else {
    error_field.innerHTML = result["description"];
  }
  return true
}

async function renderHomePage() {
document.body.innerHTML = ""
document.body.style.padding = "0 150px"

const homepageForm = document.createElement("form");
homepageForm.setAttribute("id", "homepageForm");
homepageForm.setAttribute("method", "post");
homepageForm.setAttribute("onsubmit", "return getNumber()");

// Create the container div element and set its class
const containerDiv = document.createElement("div");
containerDiv.setAttribute("class", "homepage_container");

// Create the label element and set its 'for' attribute
const label = document.createElement("label");
label.setAttribute("for", "n_operation");
label.innerHTML = "Input matrix size:";

// Create the input element and set its attributes
const input = document.createElement("input");
input.setAttribute("id", "n_operation");
input.setAttribute("type", "number");
input.setAttribute("min", "0");
input.setAttribute("required", "true");

// Create the submit button and set its attributes
const submitButton = document.createElement("button");
submitButton.setAttribute("type", "submit");
submitButton.setAttribute("class", "submitbtn");
submitButton.innerHTML = "Submit";

// Create error field
const error_field = document.createElement("h4");
error_field.setAttribute("id", "error-field");
error_field.style.color = "tomato";
error_field.innerHTML = "";

// Append the label, input, and submit button to the container div
containerDiv.appendChild(label);
containerDiv.appendChild(input);
containerDiv.appendChild(submitButton);
containerDiv.appendChild(error_field);

// Append the container div to the form
homepageForm.appendChild(containerDiv);

// Create the tasks container div and set its 'id' attribute
const tasksContainer = document.createElement("div");
tasksContainer.setAttribute("id", "tasks_container");
tasksContainer.style.backgroundColor = "white"
tasksContainer.style.borderRadius = "15px"

// Create the header div for the tasks container and set its 'id' attribute
const headerDiv = document.createElement("div");
headerDiv.setAttribute("id", "tasks_container_header");

// Create header elements and set their content
const headers = ["ID", "Input", "Status", "Result", ""];
for (const headerText of headers) {
  const header = document.createElement("h3");
  header.innerHTML = headerText;
  headerDiv.appendChild(header);
}

// Create the content div for the tasks container and set its 'id' attribute
const contentDiv = document.createElement("div");
contentDiv.setAttribute("id", "tasks_container_content");

// Append the header and content div to the tasks container
tasksContainer.appendChild(headerDiv);
tasksContainer.appendChild(contentDiv);

// Append the form and tasks container to the body
document.body.appendChild(homepageForm);
document.body.appendChild(tasksContainer);

setInterval(() => {
  if(store.buttons_counter == 0) {
    printTasks()
  }
}, 1000);
}



async function printTasks() {
  local_tasks = await getTasks();
  store.tasks = local_tasks["result"]["tasks"]

  const tasks_container = document.getElementById("tasks_container_content");

  // delete all old tasks
  
  tasks_container.innerHTML = "";
  
  store.tasks.forEach((task) => {
    
    const form_element = document.createElement("form");
    form_element.setAttribute("id", task["id"]);
  
    const id_element = document.createElement("h4");
    id_element.innerHTML = task["id"];
  
    const input_element = document.createElement("h4");
    input_element.innerHTML = task["input_data"];
  
    const status_element = document.createElement("progress");
    status_element.setAttribute("value", task["progress"]);
    status_element.setAttribute("max", "100");
  
    form_element.appendChild(id_element);
    form_element.appendChild(input_element);
    form_element.appendChild(status_element);
    form_element.style.borderBottom = "solid #9C3587"
    // result
    if (task["status"] == "error") {
      const result_element = document.createElement("h4");
      result_element.innerHTML = task["error"];
      form_element.appendChild(result_element);
    }
    else if (task["status"] == "cancelled" 
        || task["status"] == "pending"
        || task["status"] == "paused") {
  
      const result_element = document.createElement("h4");
      result_element.innerHTML = task["status"];
      form_element.appendChild(result_element);
  
    }
    else if (task["status"] == "finished") {
      const result_element = document.createElement("div");
      result_element.style.position = "relative";

      const button = document.createElement("button");
      button.setAttribute("class", "show-hide-button");
      button.setAttribute("type", "button");
      button.innerHTML = "Show More"

      const output_data = document.createElement("div");
      output_data.style.display = "none";
      output_data.style.position = "absolute";
      output_data.style.zIndex = "1";
      output_data.style.backgroundColor = "#a5a0e4";
      output_data.style.borderRadius = "5px";
      output_data.style.padding = "3px";
      
      const output_data_text = document.createElement("h5");
      output_data_text.innerHTML = task["output_data"];
      output_data_text.style.color = "ligntgrey";
      output_data_text.style.maxHeight = "100px";
      output_data_text.style.overflowY = "auto";

      output_data.appendChild(output_data_text);

      button.addEventListener('click', () => {
        if (output_data.style.display === 'none') {
          output_data.style.display = 'block';
          button.textContent = 'Hide';
          store.buttons_counter++;
      } else {
        output_data.style.display = 'none';
        button.textContent = 'Show More';
        store.buttons_counter--;
      }
      });

      
      result_element.appendChild(button)
      result_element.appendChild(output_data)
      form_element.appendChild(result_element);
    }
  
    //Cancel button
    if (task["status"] == "pending") {
      const cancelbtn = document.createElement("button");
      const div = document.createElement("div");
      cancelbtn.setAttribute("class", "cancelbtn");
      cancelbtn.setAttribute("type", "button");
      cancelbtn.innerHTML = "Cancel"
      div.appendChild(cancelbtn)
      form_element.appendChild(div)

      cancelbtn.addEventListener('click', () => {
        
        res = cancelTask(task["id"]);
        
      });

    }
  
    tasks_container.appendChild(form_element);
  });
}
