//when submitting email, returns response with appropriate json
async function submitEmail() {
  //remove any message elements from previous email inputs
  let node = document.getElementById("message");
  if (node != null) {
    node.remove();
  }

  emailInput = document.getElementById("emailInput").value;

  //validate email
  const isValidEmail = validateEmail(emailInput);

  if (!isValidEmail) {
    addElement("Please add a valid email");
    return;
  }

  try {
    //make call to backend
    const response = await fetch("/post-email", {
      method: "POST",
      body: JSON.stringify({ email: emailInput }),
    });

    const result = await response.json();

    //add element with message according to response code
    if (response.status == 200) {
      addElement(`Email accepted. Messages will be sent to ${result.email}`);
    } else if (response.status == 400) {
      addElement(result.message);
    } else {
      addElement("Oops! Something went wrong. Try again later");
    }
  } catch (err) {
    console.log(err);
    addElement("Oops! Something went wrong. Try again later");
  }
}

//add element with message from backend
function addElement(message) {
  let div = document.createElement("div");
  div.id = "message";
  div.append(message);
  document.getElementById("container").appendChild(div);
}

//validate email by regex
function validateEmail(email) {
  var re =
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}
