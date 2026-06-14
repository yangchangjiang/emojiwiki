// Cookie Consent Banner — GDPR compliant
(function(){
  if (localStorage.getItem('cookieConsent')) return;

  var banner = document.createElement('div');
  banner.id = 'cookieBanner';
  banner.style.cssText = 'position:fixed;bottom:0;left:0;right:0;background:#1e293b;border-top:1px solid #334155;padding:16px 20px;z-index:9999;display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap;font-size:0.85rem;color:#e2e8f0;';

  var text = document.createElement('p');
  text.style.cssText = 'max-width:500px;margin:0;';
  var cookieTexts = {en:"We use cookies and Google AdSense to improve your experience.",'zh-CN':"我们使用 Cookie 和 Google AdSense 来改善您的体验。",ja:"Cookie と Google AdSense を使用してエクスペリエンスを向上させています。",ko:"쿠키와 Google AdSense를 사용하여 경험을 개선합니다.",es:"Utilizamos cookies y Google AdSense para mejorar su experiencia.",pt:"Usamos cookies e Google AdSense.",fr:"Nous utilisons des cookies et Google AdSense.",de:"Wir verwenden Cookies und Google AdSense.",ar:"نحن نستخدم ملفات تعريف الارتباط و Google AdSense.",hi:"हम कुकीज़ और Google AdSense का उपयोग करते हैं।",th:"เราใช้คุกกี้และ Google AdSense",vi:"Chúng tôi sử dụng cookie và Google AdSense.",id:"Kami menggunakan cookie dan Google AdSense.",ru:"Мы используем cookie и Google AdSense."};
    text.textContent = cookieTexts[__lang || 'en'] || cookieTexts.en;

  var acceptBtn = document.createElement('button');
  var acceptTexts = {en:"Accept",'zh-CN':"接受",ja:"承諾",ko:"수락",es:"Aceptar",pt:"Aceitar",fr:"Accepter",de:"Akzeptieren",ar:"قبول",hi:"स्वीकार करें",th:"ยอมรับ",vi:"Chấp nhận",id:"Terima",ru:"Принять"};
    acceptBtn.textContent = acceptTexts[__lang || 'en'] || acceptTexts.en;
  acceptBtn.style.cssText = 'background:#10b981;color:#fff;border:none;padding:8px 18px;border-radius:8px;cursor:pointer;font-weight:600;';

  var declineBtn = document.createElement('button');
  var declineTexts = {en:"Decline",'zh-CN':"拒绝",ja:"拒否",ko:"거부",es:"Rechazar",pt:"Recusar",fr:"Refuser",de:"Ablehnen",ar:"رفض",hi:"अस्वीकार करें",th:"ปฏิเสธ",vi:"Từ chối",id:"Tolak",ru:"Отклонить"};
    declineBtn.textContent = declineTexts[__lang || 'en'] || declineTexts.en;
  declineBtn.style.cssText = 'background:#334155;color:#e2e8f0;border:1px solid #475569;padding:8px 18px;border-radius:8px;cursor:pointer;';

  acceptBtn.onclick = function(){
    localStorage.setItem('cookieConsent','accepted');
    banner.remove();
  };
  declineBtn.onclick = function(){
    localStorage.setItem('cookieConsent','declined');
    banner.remove();
  };

  banner.appendChild(text);
  banner.appendChild(acceptBtn);
  banner.appendChild(declineBtn);
  document.body.appendChild(banner);
})();
