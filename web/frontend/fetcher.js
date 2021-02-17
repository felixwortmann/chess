async function getNewFEN(fen, resultCallback) {
  var formdata = new FormData();
  formdata.append("fen", fen);

  var requestOptions = {
    method: 'POST',
    body: formdata,
    redirect: 'follow'
  };

  fetch('https://chess-ai-api.herokuapp.com/nextmove', requestOptions).then(function (response) {
    response.json().then(data => {
      return resultCallback(data);
    })

  }).catch(function (err) {
    // There was an error
    console.warn('Something went wrong.', err);
    resultCallback(err)
  });
}