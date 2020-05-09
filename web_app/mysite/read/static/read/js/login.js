function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    console.log('ID: ' + profile.getId());
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
  if (xhr.readyState == 4 && xhr.status == 200) {
    window.location = "http://localhost:8000/read/google_sign_in/";
  }
}
    xhr.open('POST', 'http://localhost:8000/read/google_sign_in/');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    //xhr.onload = function() {
        //console.log('Signed in as: ' + xhr.responseText);
    //};
    xhr.send('email=' + profile.getEmail());
}
