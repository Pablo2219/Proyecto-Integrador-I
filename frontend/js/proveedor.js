let providerMap=null,providerMarker=null,providerMode=null;

function providerEstilos(){
 const s=document.createElement('style');
 s.id='parksmart-provider-styles';
 if(document.getElementById(s.id))return;
 s.textContent=`#providerPanel{position:fixed;inset:3vh 3vw;z-index:3000;background:#f8fafc;border-radius:24px;overflow:hidden;box-shadow:0 24px 80px rgba(0,0,0,.28);display:flex;flex-direction:column}#providerPanel .provider-header{padding:18px 22px;background:#07111f;color:#fff;display:flex;align-items:center;justify-content:space-between;gap:12px}#providerPanel .provider-header h2{margin:0;font-size:22px}#providerPanel .provider-header p{margin:4px 0 0;color:#cbd5e1;font-size:13px}#providerPanel .provider-close{border:0;background:#fff2;color:#fff;border-radius:12px;padding:10px 14px;cursor:pointer}#providerPanel .provider-toolbar{padding:14px 18px;background:#fff;border-bottom:1px solid #e5e7eb;display:flex;flex-wrap:wrap;gap:10px;align-items:center}#providerPanel .provider-toolbar button{border:0;border-radius:12px;padding:10px 14px;cursor:pointer;font-weight:700}#providerPanel .provider-toolbar button.primary{background:#0f766e;color:#fff}#providerPanel .provider-toolbar button.secondary{background:#e2e8f0;color:#0f172a}#providerPanel .provider-mode{margin-left:auto;color:#475569;font-size:13px}#providerPanel .provider-body{display:grid;grid-template-columns:minmax(0,1fr) 360px;min-height:0;flex:1}#providerMap{height:100%;min-height:520px}#providerPanel .provider-side{background:#fff;border-left:1px solid #e5e7eb;padding:18px;overflow:auto}#providerPanel .provider-side h3{margin-top:0}#providerPanel .provider-hint{padding:12px;border-radius:12px;background:#f1f5f9;color:#475569;font-size:13px;margin-bottom:12px}#providerPanel .provider-coords{font:12px ui-monospace,SFMono-Regular,Menlo,monospace;color:#0f172a;background:#f8fafc;border-radius:10px;padding:8px;margin:8px 0 14px}#providerPanel .provider-form-grid{display:grid;gap:10px}#providerPanel .provider-form-grid label{display:grid;gap:6px;font-size:13px;font-weight:700;color:#334155}#providerPanel .provider-form-grid input,#providerPanel .provider-form-grid select,#providerPanel .provider-form-grid textarea{width:100%;box-sizing:border-box;border:1px solid #cbd5e1;border-radius:10px;padding:10px;background:#fff}#providerPanel .provider-form-actions{display:flex;gap:8px;margin-top:12px}#providerPanel .provider-form-actions button{flex:1;border:0;border-radius:10px;padding:10px;cursor:pointer}#providerPanel .provider-form-actions .save{background:#0f766e;color:#fff}#providerPanel .provider-form-actions .cancel{background:#e2e8f0}#providerPanel .provider-list{display:grid;gap:8px}#providerPanel .provider-item{border:1px solid #e2e8f0;border-radius:12px;padding:10px}.provider-item strong{display:block}.provider-item small{display:block;color:#64748b;margin-top:3px}@media(max-width:900px){#providerPanel .provider-body{grid-template-columns:1fr}#providerPanel .provider-side{max-height:40vh;border-left:0;border-top:1px solid #e5e7eb}#providerMap{min-height:440px}}`;
 document.head.appendChild(s);
}

function inicializarPanelProveedor(){
 providerEstilos();
 document.getElementById('providerPanel')?.remove();
 const panel=document.createElement('section');panel.id='providerPanel';
 panel.innerHTML=`<div class="provider-header"><div><h2>Panel del proveedor</h2><p>Publicá sectores y espacios directamente sobre el mapa.</p></div><button class="provider-close" type="button" onclick="cerrarPanelProveedor()">Cerrar</button></div><div class="provider-toolbar"><button class="primary" type="button" onclick="providerModoSector()">+ Añadir sector</button><button class="primary" type="button" onclick="providerModoEspacio()">+ Añadir espacio</button><button class="secondary" type="button" onclick="providerCancelarModo()">Cancelar selección</button><button class="secondary" type="button" onclick="cargarReservasProveedor()">Ver reservas</button><span id="providerModeText" class="provider-mode">Seleccioná una acción para empezar.</span></div><div class="provider-body"><div id="providerMap"></div><aside class="provider-side"><div id="providerForm"><h3>Operación</h3><div class="provider-hint">Elegí <b>Añadir sector</b> o <b>Añadir espacio</b> y después tocá el mapa en el punto exacto. Las coordenadas se toman del clic real.</div><div id="providerCoords" class="provider-coords">Latitud: —<br>Longitud: —</div><div id="providerItems" class="provider-list"></div><div id="providerReservations"></div></div></aside></div>`;
 document.body.appendChild(panel);
 providerMap=L.map('providerMap',{zoomControl:true}).setView([9.9281,-84.0907],14);
 L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'© OpenStreetMap contributors'}).addTo(providerMap);
 providerMap.on('click',providerMapaClick);
 cargarSectoresProveedor();
}

function cerrarPanelProveedor(){providerMap?.remove();providerMap=null;providerMarker=null;providerMode=null;document.getElementById('providerPanel')?.remove()}
function providerCancelarModo(){providerMode=null;providerMarker?.remove();providerMarker=null;const f=document.getElementById('providerDynamicForm');f?.remove();const c=document.getElementById('providerCoords');if(c)c.innerHTML='Latitud: —<br>Longitud: —';const m=document.getElementById('providerModeText');if(m)m.textContent='Seleccioná una acción para empezar.'}
function providerModoSector(){providerCancelarModo();providerMode='sector';document.getElementById('providerModeText').textContent='Modo sector: ahora tocá el mapa.'}
function providerModoEspacio(){providerCancelarModo();providerMode='espacio';document.getElementById('providerModeText').textContent='Modo espacio: ahora tocá el mapa.'}

function providerMapaClick(e){
 if(!providerMode){document.getElementById('providerModeText').textContent='Primero elegí Añadir sector o Añadir espacio.';return}
 const p=e.latlng;
 providerMarker?.remove();providerMarker=L.marker(p).addTo(providerMap).bindPopup(providerMode==='sector'?'Nuevo sector':'Nuevo espacio').openPopup();
 document.getElementById('providerCoords').innerHTML=`Latitud: ${p.lat.toFixed(7)}<br>Longitud: ${p.lng.toFixed(7)}`;
 renderProviderForm(providerMode,p);
}

async function cargarSectoresProveedor(){
 try{
  const data=await apiGet('/proveedores/sectores/mis-sectores');window._providerSectors=data;
  const items=document.getElementById('providerItems');
  if(items)items.innerHTML=data.map(s=>`<div class="provider-item"><strong>Sector: ${escaparHtml(s.nombreSector)}</strong><small>₡${Number(s.precioHora||0).toLocaleString('es-CR')}/hora</small><small>📍 ${Number(s.latitud).toFixed(7)}, ${Number(s.longitud).toFixed(7)}</small></div>`).join('')||'<div class="provider-hint">Aún no tenés sectores publicados.</div>';
  data.forEach(s=>L.marker([s.latitud,s.longitud]).addTo(providerMap).bindPopup(`<b>${escaparHtml(s.nombreSector)}</b><br>₡${Number(s.precioHora||0).toLocaleString('es-CR')}/hora<br>📍 ${Number(s.latitud).toFixed(7)}, ${Number(s.longitud).toFixed(7)}`));
 }catch(error){mostrarToast(limpiarMensajeError(error.message))}
}

function renderProviderForm(mode,p){
 let root=document.getElementById('providerDynamicForm');
 if(!root){root=document.createElement('div');root.id='providerDynamicForm';document.getElementById('providerForm').appendChild(root)}
 const sectors=window._providerSectors||[];
 root.innerHTML=mode==='sector'?`<h3>Crear sector</h3><form class="provider-form-grid" onsubmit="guardarSectorProveedor(event)"><label>Nombre del sector<input id="psName" required maxlength="80" placeholder="Sector Centro"></label><label>Precio por hora<input id="psPrice" type="number" min="0" step="0.01" required placeholder="1500"></label><label>Descripción<textarea id="psDesc" rows="3" maxlength="250" placeholder="Descripción del parqueo"></textarea></label><div class="provider-form-actions"><button class="cancel" type="button" onclick="providerCancelarModo()">Cancelar</button><button class="save" type="submit">Guardar sector</button></div></form>`:`<h3>Crear espacio</h3>${sectors.length?`<form class="provider-form-grid" onsubmit="guardarEspacioProveedor(event)"><label>Sector<select id="peSector" required>${sectors.map(s=>`<option value="${s.idSector}">${escaparHtml(s.nombreSector)}</option>`).join('')}</select></label><label>Código del espacio<input id="peCode" required maxlength="20" placeholder="A-01"></label><label>Tipo<select id="peType"><option value="REGULAR">Regular</option><option value="MOTOCICLETA">Motocicleta</option><option value="DISCAPACIDAD">Discapacidad</option><option value="ELECTRICO">Eléctrico</option><option value="VIP">VIP</option></select></label><div class="provider-form-actions"><button class="cancel" type="button" onclick="providerCancelarModo()">Cancelar</button><button class="save" type="submit">Guardar espacio</button></div></form>`:'<div class="provider-hint">Primero creá al menos un sector. Después podrás ubicar espacios dentro de él.</div>';
 root.dataset.lat=p.lat;root.dataset.lng=p.lng;
}

async function guardarSectorProveedor(e){e.preventDefault();const f=document.getElementById('providerDynamicForm');try{await apiPost('/proveedores/sectores',{nombreSector:document.getElementById('psName').value.trim(),descripcion:document.getElementById('psDesc').value.trim()||null,latitud:Number(f.dataset.lat),longitud:Number(f.dataset.lng),precioHora:Number(document.getElementById('psPrice').value)});mostrarToast('Sector creado correctamente.');providerCancelarModo();cargarSectoresProveedor()}catch(error){mostrarToast(limpiarMensajeError(error.message))}}
async function guardarEspacioProveedor(e){e.preventDefault();const f=document.getElementById('providerDynamicForm');try{await apiPost('/proveedores/espacios',{idSector:Number(document.getElementById('peSector').value),codigoEspacio:document.getElementById('peCode').value.trim(),tipoEspacio:document.getElementById('peType').value,latitud:Number(f.dataset.lat),longitud:Number(f.dataset.lng),descripcion:null});mostrarToast('Espacio creado correctamente.');providerCancelarModo()}catch(error){mostrarToast(limpiarMensajeError(error.message))}}

async function cargarReservasProveedor(){try{const r=await apiGet('/proveedores/reservas');document.getElementById('providerReservations').innerHTML='<h3>Reservas recibidas</h3>'+(r.map(x=>`<div class="provider-item"><strong>${escaparHtml(x.codigoReserva||'Reserva')}</strong><small>${escaparHtml(x.nombreSector||'Sector')} · ${escaparHtml(x.codigoEspacio||'Espacio')}</small><small>${new Date(x.fechaInicioReserva).toLocaleString('es-CR')} → ${new Date(x.fechaFinReserva).toLocaleString('es-CR')}</small><small>Estado: ${escaparHtml(x.estado||'—')}</small></div>`).join('')||'<div class="provider-hint">No hay reservas recibidas.</div>')}catch(error){mostrarToast(limpiarMensajeError(error.message))}}

function ocultarAccionesProveedorVehiculos(){['navVehiculos','btnVehiculos','vistaVehiculos'].forEach(id=>document.getElementById(id)?.classList.add('hidden'));document.querySelectorAll('button,a').forEach(el=>{if((el.textContent||'').trim().toLowerCase()==='vehículos')el.classList.add('hidden')})}

setTimeout(()=>{if(window.parkSmartSession?.usuario?.rol==='PROVEEDOR'){ocultarAccionesProveedorVehiculos();inicializarPanelProveedor();if(!document.getElementById('providerQuickOpen')){const b=document.createElement('button');b.id='providerQuickOpen';b.textContent='Administrar parqueos';b.onclick=inicializarPanelProveedor;b.style.cssText='position:fixed;right:20px;bottom:20px;z-index:2500;border:0;border-radius:14px;padding:12px 16px;background:#0f766e;color:#fff;font-weight:700;box-shadow:0 10px 30px #0003;cursor:pointer';document.body.appendChild(b)}}},900);