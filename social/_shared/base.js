// Shared bootstrap for social posts. Layout comes from the URL hash: #portrait | #square | #landscape.
// Post markup: <div class="post theme-indigo" id="post" data-chip="AI & TOOLS" data-icon="chat"> <div class="pad"> ...content... </div> </div>
(function(){
  const post=document.getElementById('post');
  const layout=(location.hash||'#portrait').slice(1);
  post.classList.add(layout);
  const W=post.offsetWidth,H=post.offsetHeight;

  const ICONS={
    hat:'<path d="M4 16.5a8 8 0 0 1 16 0"/><path d="M2.5 16.5h19"/><path d="M10 16.5V8.2h4v8.3"/>',
    chat:'<path d="M4 5.5h16v11H10l-5 4v-4H4z"/>',
    check:'<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    star:'<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.2 1 5.9L12 17l-5.2 2.8 1-5.9L3.5 9.7l5.9-.8z"/>',
    flag:'<path d="M6 21V4"/><path d="M6 5h11l-2 4 2 4H6"/>'
  };
  const chipText=post.dataset.chip||'DIGITRADIE';
  const icon=ICONS[post.dataset.icon||'hat'];

  // background layers
  const bg=document.createElement('div');
  bg.innerHTML='<div class="grid"></div><canvas class="stars"></canvas>'+
    '<svg class="grain" width="'+W+'" height="'+H+'"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .9 0"/></filter><rect width="100%" height="100%" filter="url(#n)"/></svg>'+
    '<div class="tape"></div>';
  while(bg.firstChild) post.insertBefore(bg.firstChild,post.firstChild);

  // top row
  const pad=post.querySelector('.pad');
  const top=document.createElement('div');top.className='top';
  top.innerHTML='<div class="brand"><img src="../../_shared/logo-circle.png"><span>DigiTradie</span></div>'+
    '<div class="chip"><svg viewBox="0 0 24 24" fill="none" stroke="#FF9A4D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'+icon+'</svg>'+chipText+'</div>';
  pad.insertBefore(top,pad.firstChild);

  // sparkles (calm: far fewer than the first post)
  const c=post.querySelector('canvas.stars');c.width=W;c.height=H;const x=c.getContext('2d');
  let s=23;const rnd=()=>{s=(s*16807)%2147483647;return s/2147483647};
  const div=post.classList.contains('theme-indigo')?36000:post.classList.contains('theme-navy')?60000:80000;
  const cols=['#ffffff','#c9b8ff','#9db4ff','#8a7bff'];
  for(let i=0;i<Math.round(W*H/div);i++){
    const px=rnd()*W,py=rnd()*H,sz=[3,3,4,4,6][Math.floor(rnd()*5)];
    x.globalAlpha=.16+rnd()*.36;x.fillStyle=cols[Math.floor(rnd()*cols.length)];x.shadowColor=x.fillStyle;x.shadowBlur=sz;x.fillRect(px,py,sz,sz);
  }
  const star=(px,py,r,a)=>{x.globalAlpha=a;x.fillStyle='#d8ccff';x.shadowColor='#8a7bff';x.shadowBlur=r*1.5;const t=r/6;x.fillRect(px-t/2,py-r,t,r*2);x.fillRect(px-r,py-t/2,r*2,t)};
  star(W*.95,H*.18,20,.6);star(W*.035,H*.55,14,.45);
})();
