function previewImage(evt){
  const out = document.getElementById('preview');
  if(!out) return;
  const file = evt.target.files[0];
  if(!file) return;
  const reader = new FileReader();
  reader.onload = (e)=>{ out.src = e.target.result; };
  reader.readAsDataURL(file);
}
function toggleNewClient(val){
  const box = document.getElementById('newClientFields');
  if(!box) return;
  if(val === 'new'){ box.classList.remove('d-none'); }
  else{ box.classList.add('d-none'); }
}
