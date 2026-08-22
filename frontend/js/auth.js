const AUTH_TOKEN_KEY='parksmart_access_token';
const AUTH_USER_KEY='parksmart_auth_user';
const AUTH_DEMO_KEY='parksmart_demo_session';
window.parkSmartSession={usuario:null,demo:false};

function obtenerTokenAcceso(){return localStorage.getItem(AUTH_TOKEN_KEY)||''}
function obtenerUsuarioGuardado(){try{return JSON.parse(localStorage.getItem(AUTH_USER_KEY)||'null')}catch{return null}}

function inyectarRegistro(){
 const login=document.querySelector('[data-auth-view="login"]');
 if(!login || document.querySelector('[data-auth-view="register"]')) return;
 const demo=login.querySelector('.auth-demo-box');
 if(demo) demo.remove();
 const cred=login.querySelector('.auth-credentials');
 if(cred) cred.remove();
 const link=document.createElement('button');
 link.className='auth-link'; link.type='button'; link.textContent='Crear una cuenta';
 link.onclick=()=>mostrarVistaAuth('register');
 login.appendChild(link);
 const panel=document.createElement('div');
 panel.dataset.authView='register'; panel.className='hidden';
 panel.innerHTML=`<button class="auth-back" type="button" onclick="mostrarVistaAuth('login')">← Volver</button>
 <span class="auth-kicker">NUEVA CUENTA</span><h1>Elegí cómo usar ParkSmart.</h1>
 <p class="auth-description">Podés registrarte como Cliente o Proveedor.</p>
 <form id="registerForm" class="auth-form">
 <label class="auth-field"><span>Tipo de cuenta</span><select id="registerRole" required><option value="CLIENTE">Cliente</option><option value="PROVEEDOR">Proveedor</option></select></label>
 <label class="auth-field"><span>Usuario</span><input id="registerUsername" type="text" minlength="4" maxlength="50" required></label>
 <label class="auth-field"><span>Correo electrónico</span><input id="registerEmail" type="email" required></label>
 <label class="auth-field"><span>Contraseña</span><input id="registerPassword" type="password" minlength="8" required></label>
 <label class="auth-field"><span>Confirmar contraseña</span><input id="registerPasswordConfirm" type="password" minlength="8" required></label>
 <div id="clientRegisterFields">
 <label class="auth-field"><span>Identificación</span><input id="registerIdentification" type="text"></label>
 <label class="auth-field"><span>Nombre</span><input id="registerName" type="text"></label>
 <label class="auth-field"><span>Primer apellido</span><input id="registerLastName" type="text"></label>
 <label class="auth-field"><span>Segundo apellido</span><input id="registerLastName2" type="text"></label>
 <label class="auth-field"><span>Teléfono</span><input id="registerPhone" type="tel"></label>
 <label class="auth-field"><span>Dirección</span><input id="registerAddress" type="text"></label></div>
 <div id="providerRegisterFields" class="hidden">
 <label class="auth-field"><span>Nombre comercial</span><input id="registerBusiness" type="text"></label>
 <label class="auth-field"><span>Identificación fiscal</span><input id="registerTaxId" type="text"></label>
 <label class="auth-field"><span>Teléfono</span><input id="registerProviderPhone" type="tel"></label>
 <label class="auth-field"><span>Dirección</span><input id="registerProviderAddress" type="text"></label></div>
 <label class="auth-field"><span><input id="registerPrivacy" type="checkbox" required> Acepto el aviso de privacidad.</span></label>
 <button id="registerButton" class="auth-primary" type="submit">Crear cuenta</button></form>`;
 document.querySelector('.auth-card')?.appendChild(panel);
 document.getElementById('registerRole')?.addEventListener('change',actualizarCamposRegistro);
 document.getElementById('registerForm')?.addEventListener('submit',registrarCuenta);
}

function actualizarCamposRegistro(){
 const provider=document.getElementById('registerRole')?.value==='PROVEEDOR';
 document.getElementById('clientRegisterFields')?.classList.toggle('hidden',provider);
 document.getElementById('providerRegisterFields')?.classList.toggle('hidden',!provider);
}

async function registrarCuenta(e){
 e.preventDefault();
 const role=document.getElementById('registerRole').value;
 const password=document.getElementById('registerPassword').value;
 const confirm=document.getElementById('registerPasswordConfirm').value;
 if(password!==confirm){mostrarMensajeAuth('Las contraseñas no coinciden.','error');return}
 const datos={nombreUsuario:document.getElementById('registerUsername').value.trim(),correoElectronico:document.getElementById('registerEmail').value.trim(),contrasena:password,rol:role,aceptaPrivacidad:document.getElementById('registerPrivacy').checked};
 if(role==='CLIENTE') Object.assign(datos,{identificacion:document.getElementById('registerIdentification').value.trim(),nombre:document.getElementById('registerName').value.trim(),primerApellido:document.getElementById('registerLastName').value.trim(),segundoApellido:document.getElementById('registerLastName2').value.trim()||null,telefono:document.getElementById('registerPhone').value.trim(),direccion:document.getElementById('registerAddress').value.trim()||null});
 else Object.assign(datos,{nombreComercial:document.getElementById('registerBusiness').value.trim(),identificacionFiscal:document.getElementById('registerTaxId').value.trim()||null,telefono:document.getElementById('registerProviderPhone').value.trim(),direccion:document.getElementById('registerProviderAddress').value.trim()||null});
 const button=document.getElementById('registerButton'); button.disabled=true; button.textContent='Creando...';
 try{const respuesta=await apiPost('/auth/registro',datos);guardarSesionAutenticada(respuesta.accessToken,respuesta.usuario);window.location.reload();}
 catch(error){mostrarMensajeAuth(limpiarMensajeError(error.message),'error');}
 finally{button.disabled=false;button.textContent='Crear cuenta';}
}

async function inicializarAutenticacion(){
 inyectarRegistro();
 configurarEventosAutenticacion();
 localStorage.removeItem(AUTH_DEMO_KEY);
 const tokenReset=new URLSearchParams(window.location.search).get('reset_token');
 if(tokenReset){mostrarPantallaAuth('reset');document.getElementById('resetToken').value=tokenReset;return false}
 const token=obtenerTokenAcceso();
 if(!token){mostrarPantallaAuth('login');return false}
 try{const usuario=await apiGet('/auth/me');guardarSesionAutenticada(token,usuario);activarSesionVisual(usuario,false);return true}
 catch(error){limpiarSesionAutenticada();mostrarPantallaAuth('login');mostrarMensajeAuth('La sesión expiró. Iniciá sesión nuevamente.','error');return false}
}

function configurarEventosAutenticacion(){
 if(window.authEventsConfigured)return;
 window.authEventsConfigured=true;
 document.getElementById('loginForm')?.addEventListener('submit',iniciarSesion);
 document.getElementById('recoveryForm')?.addEventListener('submit',solicitarRestablecimiento);
 document.getElementById('resetForm')?.addEventListener('submit',restablecerContrasena);
 document.getElementById('changePasswordForm')?.addEventListener('submit',cambiarContrasena);
 document.getElementById('adminUserForm')?.addEventListener('submit',crearUsuarioDesdeAdmin);
 document.getElementById('adminNotificationForm')?.addEventListener('submit',enviarNotificacionDesdeAdmin);
}

function mostrarPantallaAuth(vista='login'){
 document.getElementById('authScreen')?.classList.remove('hidden');document.getElementById('appShell')?.classList.add('hidden');
 document.querySelectorAll('[data-auth-view]').forEach(panel=>panel.classList.toggle('hidden',panel.dataset.authView!==vista));
 const mensaje=document.getElementById('authMessage');if(mensaje)mensaje.className='auth-message hidden';
}
function mostrarVistaAuth(vista){mostrarPantallaAuth(vista)}

function activarSesionVisual(usuario){
 window.parkSmartSession.usuario=usuario;window.parkSmartSession.demo=false;
 document.getElementById('authScreen')?.classList.add('hidden');document.getElementById('appShell')?.classList.remove('hidden');
 document.body.classList.toggle('admin-session',usuario.rol==='ADMINISTRADOR');
 const roleChip=document.getElementById('profileRole');if(roleChip)roleChip.textContent=usuario.rol==='ADMINISTRADOR'?'Administrador':usuario.rol==='PROVEEDOR'?'Proveedor':'Cliente';
 document.getElementById('adminToolsButton')?.classList.toggle('hidden',usuario.rol!=='ADMINISTRADOR');
 const roleDescription=document.getElementById('rolDescripcion');if(roleDescription)roleDescription.textContent=usuario.rol==='PROVEEDOR'?'Administrá tus sectores, espacios y reservas recibidas.':usuario.rol==='ADMINISTRADOR'?'Administrá usuarios, proveedores y operación.':'Buscá, reservá y gestioná tus espacios.';
 document.getElementById('providerDashboard')?.classList.toggle('hidden',usuario.rol!=='PROVEEDOR');
 document.getElementById('clientHomeSection')?.classList.toggle('hidden',usuario.rol==='PROVEEDOR');
 document.getElementById('adminHomeSection')?.classList.toggle('hidden',usuario.rol!=='ADMINISTRADOR');
}

async function iniciarSesion(e){e.preventDefault();const boton=document.getElementById('loginButton');boton.disabled=true;boton.textContent='Verificando...';try{const respuesta=await apiPost('/auth/login',{usuario:document.getElementById('loginUser').value.trim(),contrasena:document.getElementById('loginPassword').value});guardarSesionAutenticada(respuesta.accessToken,respuesta.usuario);window.location.reload()}catch(error){mostrarMensajeAuth(limpiarMensajeError(error.message),'error')}finally{boton.disabled=false;boton.textContent='Iniciar sesión'}}
function guardarSesionAutenticada(token,usuario){localStorage.setItem(AUTH_TOKEN_KEY,token);localStorage.setItem(AUTH_USER_KEY,JSON.stringify(usuario));if(usuario.idCliente)localStorage.setItem('parksmart_cliente_id',String(usuario.idCliente));window.parkSmartSession.usuario=usuario}
function limpiarSesionAutenticada(){localStorage.removeItem(AUTH_TOKEN_KEY);localStorage.removeItem(AUTH_USER_KEY);localStorage.removeItem(AUTH_DEMO_KEY)}
async function cerrarSesion(){try{if(obtenerTokenAcceso())await apiPost('/auth/logout',{})}catch{}limpiarSesionAutenticada();sessionStorage.clear();window.location.reload()}
function cambiarCuenta(){cerrarSesion()}
function mostrarMensajeAuth(mensaje,tipo='success'){const elemento=document.getElementById('authMessage');if(elemento){elemento.textContent=mensaje;elemento.className=`auth-message ${tipo}`}}

async function solicitarRestablecimiento(e){e.preventDefault();const boton=document.getElementById('recoveryButton');if(boton)boton.disabled=true;try{const respuesta=await apiPost('/auth/solicitar-restablecimiento',{usuarioOCorreo:document.getElementById('recoveryIdentity').value.trim(),canal:document.getElementById('recoveryChannel').value});mostrarMensajeAuth(respuesta.mensaje,'success');if(respuesta.tokenRestablecimiento){document.getElementById('resetToken').value=respuesta.tokenRestablecimiento;mostrarVistaAuth('reset')}}catch(error){mostrarMensajeAuth(limpiarMensajeError(error.message),'error')}finally{if(boton)boton.disabled=false}}
async function restablecerContrasena(e){e.preventDefault();const nueva=document.getElementById('resetPassword').value,confirmacion=document.getElementById('resetPasswordConfirm').value;if(nueva!==confirmacion){mostrarMensajeAuth('Las contraseñas no coinciden.','error');return}try{const respuesta=await apiPost('/auth/restablecer-contrasena',{token:document.getElementById('resetToken').value.trim(),nuevaContrasena:nueva});window.history.replaceState({},'',window.location.pathname);mostrarVistaAuth('login');mostrarMensajeAuth(respuesta.mensaje,'success')}catch(error){mostrarMensajeAuth(limpiarMensajeError(error.message),'error')}}
function abrirCambioContrasena(){document.getElementById('changePasswordForm')?.reset();abrirDialogo('changePasswordDialog')}
async function cambiarContrasena(e){e.preventDefault();if(newPassword.value!==confirmNewPassword.value){mostrarToast('Las contraseñas nuevas no coinciden.');return}try{const r=await apiPut('/auth/cambiar-contrasena',{contrasenaActual:currentPassword.value,nuevaContrasena:newPassword.value});cerrarDialogo('changePasswordDialog');mostrarToast(r.mensaje)}catch(error){mostrarToast(limpiarMensajeError(error.message))}}
async function abrirAdministracion(){if(window.parkSmartSession.usuario?.rol!=='ADMINISTRADOR')return;abrirDialogo('adminDialog');await cargarUsuariosAdmin()}
async function cargarUsuariosAdmin(){const contenedor=document.getElementById('adminUsersList');if(!contenedor)return;contenedor.innerHTML='Cargando usuarios...';try{const usuarios=await apiGet('/usuarios/');contenedor.innerHTML=usuarios.map(usuario=>`<article class="admin-user-row"><strong>${escaparHtml(usuario.nombreUsuario)}</strong><small>${escaparHtml(usuario.correoElectronico)}</small><span>${formatearEstado(usuario.rol)}</span></article>`).join('')}catch(error){contenedor.textContent=limpiarMensajeError(error.message)}}
async function crearUsuarioDesdeAdmin(e){e.preventDefault();try{const rol=document.getElementById('adminUserRole').value,id=document.getElementById('adminUserClientId').value.trim();await apiPost('/usuarios/',{nombreUsuario:document.getElementById('adminUsername').value.trim(),correoElectronico:document.getElementById('adminUserEmail').value.trim(),contrasena:document.getElementById('adminUserPassword').value,rol,idCliente:id?Number(id):null});e.target.reset();mostrarToast('Usuario creado correctamente');await cargarUsuariosAdmin()}catch(error){mostrarToast(limpiarMensajeError(error.message))}}
async function enviarNotificacionDesdeAdmin(e){e.preventDefault();try{await apiPost('/notificaciones/',{idCliente:Number(document.getElementById('adminNotificationClientId').value),tipoNotificacion:'SISTEMA',canal:document.getElementById('adminNotificationChannel').value,titulo:document.getElementById('adminNotificationTitle').value.trim(),mensaje:document.getElementById('adminNotificationMessage').value.trim(),destinatario:document.getElementById('adminNotificationRecipient').value.trim()||null,enviarAhora:true});e.target.reset();mostrarToast('Notificación enviada')}catch(error){mostrarToast(limpiarMensajeError(error.message))}}

document.addEventListener('DOMContentLoaded',()=>{inyectarRegistro()});
