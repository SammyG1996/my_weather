const progressBar = document.querySelector('#progress-bar');


async function get_ip(){
  let data = await axios.get('https://api.ipify.org?format=json');
  await axios.get('/search', {params: {q : data.data['ip']}});

  window.location.replace("/weather_search");
}

if (progressBar) {
  get_ip()
}
