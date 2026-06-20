(function(){
var BASE=window.location.pathname.match(/^\/[^\/]+\//)||["/"];
if(BASE[0]==="/")BASE="/";else BASE=BASE[0];
var L=["zh-CN","ja","ko","ru"];
function goLang(l){
  var p=window.location.pathname;
  for(var i=0;i<L.length;i++){
    if(p.indexOf("/"+L[i]+"/")>=0){
      if(l==="en"){window.location.href=p.replace("/"+L[i]+"/","/")}
      else{window.location.href=p.replace("/"+L[i]+"/","/"+l+"/")}
      return
    }
  }
  var parts=p.split("/").filter(function(x){return x.length>0});
  var pg=parts.join("/")||"index.html";
  if(l==="en"){window.location.href="/"+pg}
  else{window.location.href="/"+l+"/"+pg}
}
var btn=document.createElement("div");
btn.className="lang-wrap";
btn.innerHTML='<button class="lang-btn" onclick="this.nextElementSibling.classList.toggle(\'show\')">\ud83c\udf10</button><div class="lang-dropdown"><button onclick="goLang(\'en\')">English</button><button onclick="goLang(\'zh-CN\')">\u7b80\u4f53\u4e2d\u6587</button><button onclick="goLang(\'ja\')">\u65e5\u672c\u8a9e</button><button onclick="goLang(\'ko\')">\ud55c\uad6d\uc5b4</button><button onclick="goLang(\'ru\')">\u0420\u0443\u0441\u0441\u043a\u0438\u0439</button></div>';
document.addEventListener("DOMContentLoaded",function(){
  var nav=document.querySelector("nav");if(document.querySelector(".lang-wrap"))return;
  if(nav)nav.insertBefore(btn,nav.firstChild);
  var style=document.createElement("style");
  style.textContent=".lang-wrap{position:relative;margin-right:12px}.lang-btn{background:0 0;border:1px solid var(--border);padding:6px 12px;border-radius:8px;cursor:pointer;font-size:.85rem;color:var(--text)}.lang-dropdown{display:none;position:absolute;top:100%;left:0;background:var(--surface);border:1px solid var(--border);border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,.12);z-index:999;min-width:140px;padding:4px 0}.lang-dropdown.show{display:block}.lang-dropdown button{display:block;width:100%;text-align:left;padding:6px 16px;border:none;background:0 0;font-size:.85rem;cursor:pointer;color:var(--text)}.lang-dropdown button:hover{background:var(--accent-bg)}";
  document.head.appendChild(style);
  document.addEventListener("click",function(e){if(!e.target.closest(".lang-wrap")){var d=document.querySelector(".lang-dropdown");if(d)d.classList.remove("show")}});
});
})();
