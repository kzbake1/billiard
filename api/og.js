import { ImageResponse } from '@vercel/og';
export const config = { runtime: 'edge' };
const SB='https://dhsrklircobualygdacz.supabase.co',KEY='sb_publishable_CoPq83PXPQWtfTzMECB7jg_VI-tjPyM';
const MON=['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'];
const pl=(n,a,b,c)=>{const m=n%10,h=n%100;return m===1&&h!==11?a:m>=2&&m<=4&&(h<10||h>=20)?b:c};
const h=(type,style,children,extra)=>({type,props:Object.assign({style},extra||{},children===undefined?{}:{children})});
async function get(path){try{const r=await fetch(SB+'/rest/v1/'+path,{headers:{apikey:KEY,Authorization:'Bearer '+KEY}});return r.ok?await r.json():[]}catch(e){return[]}}
const b64=s=>{let b='';const u=new TextEncoder().encode(s);for(let i=0;i<u.length;i++)b+=String.fromCharCode(u[i]);return btoa(b)};
export default async function handler(req){
  const u=new URL(req.url),base=u.origin;
  const id=String(u.searchParams.get('id')||'').replace(/[^a-z0-9]/g,'').slice(0,40);
  let title='Бильярдные турниры',top='kazbilliard.com',info='',st='',stc='#1667FF';
  if(id){const [t]=await get('tournament?select=data,club_id&deleted_at=is.null&id=eq.'+id);
    if(t&&t.data){const d=t.data;const [c]=await get('club?select=name,city&id=eq.'+encodeURIComponent(t.club_id));
      title=d.title||title;const tp=[];
      if(d.date){const [y,m,dd]=String(d.date).split('-');if(m)tp.push((+dd)+' '+MON[+m-1]+' '+y)}
      if(c&&c.city)tp.push(c.city);top=tp.join(' · ');
      const ip=[];if(c&&c.name)ip.push(c.name);const n=(d.players||[]).length;
      if(n)ip.push(d.pair?n+' '+pl(n,'пара','пары','пар'):n+' '+pl(n,'участник','участника','участников'));
      if(d.discipline)ip.push(d.discipline);info=ip.join(' · ');
      if(d.status==='reg'){st='Идёт регистрация';stc='#1667FF'}else if(d.status==='live'||d.status==='paused'){st='Идёт игра';stc='#D93A26'}else if(d.status==='done'||d.status==='archived'){st='Завершён';stc='#0B7A47'}}}
  const [f1,f3,logo,pat]=await Promise.all(['inter-500.ttf','inter-600.ttf'].map(f=>fetch(base+'/og/'+f).then(r=>r.arrayBuffer())).concat([fetch(base+'/logo-white.svg').then(r=>r.text()),fetch(base+'/pattern-blue.svg').then(r=>r.text())]));
  const patU='data:image/svg+xml;base64,'+b64(pat),logoU='data:image/svg+xml;base64,'+b64(logo);
  const fs=title.length>48?56:title.length>32?64:72;
  const tiles=[];for(const x of [0,640])for(const y of [0,320])tiles.push(h('img',{position:'absolute',left:x,top:y,width:640,height:320},undefined,{src:patU,width:640,height:320}));
  const el=h('div',{width:1200,height:630,display:'flex',position:'relative',background:'#1667FF',fontFamily:'Inter'},[
    ...tiles,
    h('div',{position:'absolute',left:0,top:0,width:1200,height:630,padding:'64px 72px',display:'flex',flexDirection:'column',justifyContent:'space-between'},[
      h('div',{display:'flex',justifyContent:'space-between',alignItems:'center'},[
        h('img',{height:56,width:233},undefined,{src:logoU,width:233,height:56}),
        st?h('div',{display:'flex',alignItems:'center',background:'#fff',borderRadius:999,padding:'12px 24px',fontSize:26,fontWeight:600,color:'#111111'},[h('div',{width:14,height:14,borderRadius:7,background:stc,marginRight:12}),st]):h('div',{display:'flex'})]),
      h('div',{display:'flex',flexDirection:'column',alignItems:'flex-start'},[
        top?h('div',{color:'#C9DAFF',fontSize:24,fontWeight:600,letterSpacing:1.5,textTransform:'uppercase'},top):null,
        h('div',{color:'#fff',fontSize:fs,fontWeight:500,lineHeight:1.08,margin:'14px 0 26px',lineClamp:2,display:'block',maxWidth:1056},title),
        info?h('div',{display:'flex',background:'#fff',borderRadius:12,padding:'14px 22px',fontSize:26,fontWeight:500,color:'#111111'},info):null].filter(Boolean))])]);
  return new ImageResponse(el,{width:1200,height:630,fonts:[{name:'Inter',data:f1,weight:500},{name:'Inter',data:f3,weight:600}],headers:{'Cache-Control':'public, max-age=300, s-maxage=300, stale-while-revalidate=600'}});
}
