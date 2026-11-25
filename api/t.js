const SB='https://dhsrklircobualygdacz.supabase.co',KEY='sb_publishable_CoPq83PXPQWtfTzMECB7jg_VI-tjPyM';
const MON=['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'];
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const pl=(n,a,b,c)=>{const m=n%10,h=n%100;return m===1&&h!==11?a:m>=2&&m<=4&&(h<10||h>=20)?b:c};
async function get(path){const r=await fetch(SB+'/rest/v1/'+path,{headers:{apikey:KEY,Authorization:'Bearer '+KEY}});if(!r.ok)return[];return r.json()}
module.exports=async(req,res)=>{
  const id=String((req.query&&req.query.id)||'').replace(/[^a-z0-9]/g,'').slice(0,40);
  const to='/#t-'+id;
  let sk='';let title='kazbilliard — бильярдные турниры',desc='Первая казахстанская платформа бильярдных турниров: сетка, счёт и столы онлайн.';
  try{
    if(id){const [t]=await get('tournament?select=data,club_id&deleted_at=is.null&id=eq.'+id);
      if(t&&t.data){const d=t.data;const [c]=await get('club?select=name&id=eq.'+encodeURIComponent(t.club_id));
        title=d.title||title;const parts=[];
        const st=d.status==='reg'?'Идёт регистрация':d.status==='live'||d.status==='paused'?'Идёт игра':d.status==='done'||d.status==='archived'?'Завершён':'';if(st)parts.push(st);sk=d.status||'';
        if(c&&c.name)parts.push(c.name);
        if(d.date){const [y,m,dd]=d.date.split('-');if(m)parts.push((+dd)+' '+MON[+m-1]+' '+y)}
        const n=(d.players||[]).length;if(n)parts.push(d.pair?n+' '+pl(n,'пара','пары','пар'):n+' '+pl(n,'участник','участника','участников'));
        if(d.discipline)parts.push(d.discipline+(d.pair?' · парный':''));
        desc=parts.join(' · ')||desc}}
  }catch(e){}
  const host=/^([a-z0-9-]+\.)?kazbilliard\.com$/.test(String(req.headers&&req.headers.host||''))?req.headers.host:'kazbilliard.com';
  const url='https://'+host+'/t/'+id,img='https://'+host+'/api/og?id='+id+'&s='+encodeURIComponent(sk);
  const fs=require('fs'),path=require('path');let page=fs.readFileSync(path.join(__dirname,'..','index.html'),'utf8');
  const T=esc(title),D=esc(desc);
  page=page.replace(/<title>[^<]*<\/title>/,'<title>'+T+' — kazbilliard</title>')
    .replace(/<meta name="description" content="[^"]*">/g,'<meta name="description" content="'+D+'">')
    .replace(/<meta property="og:title" content="[^"]*">/g,'<meta property="og:title" content="'+T+'">')
    .replace(/<meta property="og:description" content="[^"]*">/g,'<meta property="og:description" content="'+D+'">')
    .replace(/<meta property="og:image" content="[^"]*">/g,'<meta property="og:image" content="'+img+'">')
    .replace('<meta property="og:type" content="website">','<meta property="og:type" content="website"><meta property="og:url" content="'+url+'"><meta property="og:image:type" content="image/png">');
  res.setHeader('Content-Type','text/html; charset=utf-8');
  res.setHeader('Cache-Control','public, s-maxage=30, stale-while-revalidate=30');
  res.status(200).send(page)};
