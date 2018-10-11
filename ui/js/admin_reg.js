//Fetch API script for usage in the front end pages

//Register an Admin
document.getElementById("admin_register").addEventListener("click",adminDetails);

function adminDetails(){
    username = document.getElementById("user").value;
    email = document.getElementById("email").value;
    phone = document.getElementById("phone").value;
    vendor = document.getElementById("vendor").value;
    local = document.getElementById("local").value;
    pass_original = document.getElementById("pass_original").value;
    pass_confirm = document.getElementById("pass_confirm").value;
    if(pass_confirm == pass_original){
        //Check if data entered correctly
        if( username != "" && email != "" && phone != "" && vendor != "" && local != "" && pass_original != "" ){
            registerAdmin(username, email, phone, vendor, local, pass_original)

        }else{
            alert("Please ensure all fields are filled.");

        }
    }else{
        alert("Your Passwords don't match");
    }
}

function registerAdmin(username, email, phone, vendor, local, password){
    options = {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body:JSON.stringify({
            "type": "ADMIN",
            "name": username,
            "vendor_name": vendor,
            "password": password,
            "about": "This is about me",
            "location": local,
            "image_url": "NON",
            "phone_no": phone,
            "email": email
        }),
        mode: "no-cors" 
    }

    fetch("http://127.0.0.1:5000/auth/signup",options)
    .then(response => {
        return response.text()
      })
      .then((data) => {
          console.log(JSON.parse(data))
      })
      .catch((error) => {
        console.log(error)
      });
}