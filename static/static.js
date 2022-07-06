const hiddenAddress = document.querySelector('#hidden-address');
const hiddenForm = document.querySelector('#hidden-form');

async function get_ip(){
  data = await axios.get('https://api.ipify.org?format=json');
  hiddenAddress.value = data.data['ip'];
  hiddenForm.submit();

}

if (hiddenForm !== null) {
  get_ip();
}


