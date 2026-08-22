document.addEventListener('DOMContentLoaded',()=>{
 const map={btnDashboard:'cargarDashboard',btnClientes:'cargarClientes',btnVehiculos:'cargarVehiculos',btnReservas:'cargarReservas',btnPagos:'cargarPagos',btnDeudas:'cargarDeudas',btnNotificaciones:'cargarNotificaciones'};
 Object.entries(map).forEach(([id,fn])=>document.getElementById(id)?.addEventListener('click',()=>window[fn]?.()));
 window.cargarDashboard?.();
 const s=document.createElement('script');s.src='js/roles.js';s.onload=()=>window.prepararRegistroCuenta?.();document.body.appendChild(s);
});
