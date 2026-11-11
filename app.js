(function(){
'use strict';
var OWNER='sigco3111',PAGE=60,INDEX='assets-index.min.json',CSV='catalog.csv';
var REPOS=[['','','전체'],['2d','assets-2d-pixel','2D·텍스처'],['3d','assets-3d-lowpoly','3D'],['ui','assets-ui-icons','UI·아이콘'],['audio','assets-audio','오디오'],['portrait','assets-2d-portraits','초상화']];
var REPO_BY_KEY={},KEY_BY_REPO={},SHORT={'assets-2d-pixel':'2D','assets-3d-lowpoly':'3D','assets-ui-icons':'UI','assets-audio':'오디오','assets-2d-portraits':'초상화'};
REPOS.forEach(function(r,i){if(r[0]){REPO_BY_KEY[r[0]]=r[1];KEY_BY_REPO[r[1]]=r[0]}});
var REPO_ORDER={};REPOS.forEach(function(r,i){if(r[1])REPO_ORDER[r[1]]=i});
var CAT_LABEL={effect:'이펙트',sfx:'효과음',music:'음악',voice:'음성',
  'tileset-2d':'2D 타일셋','sprite-2d':'2D 스프라이트','background-2d':'2D 배경','map-2d':'2D 맵',
  ui:'UI',icon:'아이콘',portrait:'초상화',font:'폰트',texture:'텍스처',
  'model-3d':'3D 모델','character-3d':'3D 캐릭터','vehicle-3d':'3D 탈것','building-3d':'3D 건물',
  board:'보드게임',puzzle:'퍼즐',other:'기타'};
var CAT_ORDER=Object.keys(CAT_LABEL);
var LIC_LABEL={cc0:'CC0','cc-by':'CC BY',mit:'MIT',gpl:'GPL',other:'기타'};
var LIC_ORDER=['cc0','cc-by','mit','gpl','other'];
var FX=[['hit','타격·충격',['hit','impact']],['magic','마법',['magic']],['explosion','폭발',['explosion']],['lightning','번개',['lightning']],['fire','불',['fire']],['ice','얼음',['ice']],['wind','바람',['wind']],['heal','치유',['heal']],['laser','레이저',['laser']],['particle','입자',['particle']],['smoke','연기',['smoke']],['aura','오라',['aura']],['projectile','투사체',['projectile']],['slash','베기',['slash']]];
var FX_KEYS={},FX_KO={};
FX.forEach(function(f){FX_KEYS[f[0]]=f[2];f[2].forEach(function(k){FX_KO[k]=f[1]})});
var FX_ALIAS={impact:'hit'};
var SYN={'던전':['dungeon'],'나무':['tree','nature','forest'],'숲':['forest','nature'],'칼':['sword','weapon'],'검':['sword','weapon'],'무기':['weapon'],'총':['gun','shooter','blaster'],'캐릭터':['character'],'몬스터':['monster','creature','zombie'],'적':['enemy'],'도시':['city','town','urban'],'마을':['town','village'],'집':['house','building'],'건물':['building'],'자동차':['car','vehicle','racing'],'탈것':['vehicle'],'우주':['space','scifi'],'로봇':['robot'],'음식':['food'],'농작물':['crops','farm'],'효과음':['sfx','sound'],'음악':['music'],'아이콘':['icon','icons'],'버튼':['button','ui'],'배경':['background'],'타일':['tile','tileset'],'퍼즐':['puzzle'],'픽셀':['pixel'],'물고기':['fish'],'동물':['animal','animals'],'배':['ship','boat'],'비행기':['plane','aircraft'],'해적':['pirate'],'좀비':['zombie'],'판타지':['fantasy'],'중세':['medieval'],'폭발':['explosion','explode','blast'],'이펙트':['effect','effects','particles'],'음성':['voice'],'인터페이스':['interface','ui'],
  '타격':['hit'],'충격':['impact'],'마법':['magic','spell'],'번개':['lightning','thunder'],'불':['fire','flame'],'얼음':['ice','frost'],'바람':['wind'],'치유':['heal','healing'],'레이저':['laser'],'입자':['particle','particles'],'연기':['smoke'],'오라':['aura'],'투사체':['projectile'],'베기':['slash']};
var DEF={q:'',cat:'',repo:'',lic:'',fx:[],sort:'new',author:'',noattr:false,noai:false};
var all=[],list=[],shown=0,state=clone(DEF),usedCsv=false,nameCount={};
var $=function(id){return document.getElementById(id)};

function clone(o){return {q:o.q,cat:o.cat,repo:o.repo,lic:o.lic,fx:o.fx.slice(),sort:o.sort,author:o.author,noattr:o.noattr,noai:o.noai}}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function safeUrl(u){return /^https?:\/\//i.test(u||'')?u:''}
function fmt(n){return n.toLocaleString('ko-KR')}

/* ---------- data ---------- */
function parseCSV(t){
  var out=[],row=[],f='',q=false,i=0;
  if(t.charCodeAt(0)===0xFEFF)t=t.slice(1);
  for(;i<t.length;i++){var c=t[i];
    if(q){if(c==='"'){if(t[i+1]==='"'){f+='"';i++}else q=false}else f+=c}
    else if(c==='"')q=true;
    else if(c===','){row.push(f);f=''}
    else if(c==='\n'||c==='\r'){if(c==='\r'&&t[i+1]==='\n')i++;row.push(f);f='';if(row.length>1||row[0]!=='')out.push(row);row=[]}
    else f+=c}
  if(f!==''||row.length){row.push(f);out.push(row)}
  var h=out.shift();
  return out.map(function(r){var o={};h.forEach(function(k,j){o[k.trim()]=(r[j]||'').trim()});return o});
}
function famOf(l){l=l||'';if(/^CC0/i.test(l))return 'cc0';if(/CC[- ]?BY/i.test(l))return 'cc-by';if(/MIT/i.test(l))return 'mit';if(/GPL/i.test(l))return 'gpl';return 'other'}
function csvToAsset(r){
  var f=r.file||'',url=/^https?:/.test(f)?f:(f?'https://github.com/'+OWNER+'/'+r.repo+(f.indexOf('releases/')===0?'/'+f:'/raw/main/'+f):'');
  var urls=url?[url]:[];
  if(r.split&&url){var b=url.replace(/[^\/]*$/,'');urls=r.split.split(';').map(function(x){return x.trim()}).filter(Boolean).map(function(x){return b+x})}
  var fam=famOf(r.license);
  return {id:r.repo+'/'+r.name,name:r.name,repo:r.repo,file:f,type:r.type,category:'other',tags:(r.tags||'').split(',').map(function(t){return t.trim()}).filter(Boolean),effect_kind:[],author:r.author,source_url:r.source_url,license:r.license,license_family:fam,license_note:null,attribution:r.attribution,attribution_required:fam!=='cc0'&&!/^optional/i.test(r.attribution||''),ai_generated:false,added:r.added,notes:r.notes,preview:r.preview||null,sample:r.sample||null,multipart:urls.length>1,split_parts:[],download_path:f,download_url:urls.length===1?urls[0]:null,download_urls:urls};
}
function prep(a){
  var rows=(Array.isArray(a)?a:[]).filter(function(r){return r&&(r.name||r.file)});
  rows.forEach(function(r,i){
    r._i=i;r.tags=Array.isArray(r.tags)?r.tags:[];r.effect_kind=Array.isArray(r.effect_kind)?r.effect_kind:[];
    r.download_urls=(Array.isArray(r.download_urls)?r.download_urls:[]).filter(safeUrl);
    r._cat=CAT_LABEL[r.category]||r.category||'';
    r._s=[r.name,r.tags.join(' '),r.author,r.notes,r.effect_kind.join(' '),r.effect_kind.map(function(k){return FX_KO[k]||''}).join(' '),r.type,r._cat].join(' \n ').toLowerCase();
    r._fx=r.effect_kind.map(function(k){return FX_ALIAS[k]||k});
    var n=(r.name||'').toLowerCase();nameCount[n]=(nameCount[n]||0)+1;
  });
  return rows;
}
function getJSON(){
  return fetch(INDEX).then(function(r){if(!r.ok)throw new Error('HTTP '+r.status);return r.json()}).then(function(d){
    var a=Array.isArray(d)?d:(d&&d.assets);
    if(!Array.isArray(a)||!a.length)throw new Error('빈 색인');
    return a});
}
function getCSV(){
  return fetch(CSV).then(function(r){if(!r.ok)throw new Error('HTTP '+r.status);return r.text()}).then(function(t){
    var a=parseCSV(t).filter(function(r){return r.name||r.file}).map(csvToAsset);
    if(!a.length)throw new Error('빈 카탈로그');
    usedCsv=true;return a});
}
function load(){
  $('loading').hidden=false;$('error').hidden=true;$('sub').textContent='불러오는 중…';
  document.body.setAttribute('aria-busy','true');
  getJSON().catch(function(e){console.warn('assets-index.min.json 실패, catalog.csv로 대체',e);return getCSV()}).then(function(a){
    all=prep(a);init();
  }).catch(function(e){
    console.error(e);
    $('loading').hidden=true;document.body.removeAttribute('aria-busy');
    $('sub').textContent='에셋 색인을 불러오지 못했습니다.';
    var b=$('error');b.hidden=false;b.innerHTML='에셋 색인(assets-index.min.json)과 catalog.csv를 모두 불러오지 못했습니다. 네트워크를 확인한 뒤 다시 시도하세요. <button type="button" id="retry">다시 시도</button>';
    $('retry').addEventListener('click',load);
  });
}

/* ---------- search / filter / sort ---------- */
function termAlts(t){var s=SYN[t];if(!s)return [t];return t.length>1?s.concat([t]):s}
function filtered(){
  var terms=state.q.toLowerCase().split(/\s+/).filter(Boolean).map(termAlts),repo=state.repo?REPO_BY_KEY[state.repo]:'';
  var fx=state.fx;
  var out=all.filter(function(r){
    if(repo&&r.repo!==repo)return false;
    if(state.cat&&r.category!==state.cat)return false;
    if(state.lic&&r.license_family!==state.lic)return false;
    if(state.author&&r.author!==state.author)return false;
    if(state.noattr&&r.attribution_required)return false;
    if(state.noai&&r.ai_generated)return false;
    if(fx.length&&!fx.some(function(k){return r._fx.indexOf(k)>=0}))return false;
    for(var i=0;i<terms.length;i++){var alts=terms[i],hit=false;for(var j=0;j<alts.length;j++){if(r._s.indexOf(alts[j])>=0){hit=true;break}}if(!hit)return false}
    return true});
  var col=new Intl.Collator('ko',{numeric:true,sensitivity:'base'});
  if(state.sort==='name')out.sort(function(a,b){return col.compare(a.name,b.name)});
  else if(state.sort==='type')out.sort(function(a,b){return (REPO_ORDER[a.repo]||9)-(REPO_ORDER[b.repo]||9)||col.compare(a.type||'',b.type||'')||col.compare(a.name,b.name)});
  else out.sort(function(a,b){return (b.added||'').localeCompare(a.added||'')||b._i-a._i});
  return out}

/* ---------- URL state ---------- */
function toParams(s){
  var p=new URLSearchParams();
  if(s.q)p.set('q',s.q);if(s.cat)p.set('cat',s.cat);if(s.repo)p.set('repo',s.repo);if(s.lic)p.set('lic',s.lic);
  if(s.fx.length)p.set('fx',s.fx.join(','));if(s.sort!=='new')p.set('sort',s.sort);
  if(s.author)p.set('author',s.author);if(s.noattr)p.set('noattr','1');if(s.noai)p.set('ai','0');
  return p}
function fromURL(){
  var s=clone(DEF),p=new URLSearchParams(location.search);
  s.q=p.get('q')||'';
  var c=p.get('cat');if(c&&CAT_LABEL[c])s.cat=c;
  var r=p.get('repo');if(r){if(REPO_BY_KEY[r])s.repo=r;else if(KEY_BY_REPO[r])s.repo=KEY_BY_REPO[r]}
  var l=p.get('lic');if(l&&LIC_LABEL[l])s.lic=l;
  var f=p.get('fx');if(f)f.split(',').forEach(function(k){k=FX_ALIAS[k]||k;if(FX_KEYS[k]&&s.fx.indexOf(k)<0)s.fx.push(k)});
  var so=p.get('sort');if(so==='name'||so==='type')s.sort=so;
  s.author=p.get('author')||'';
  s.noattr=p.get('noattr')==='1';s.noai=p.get('ai')==='0';
  if(location.hash.length>2&&location.search===''){ /* 예전 주소(#{"q":..}) 호환 */
    try{var h=JSON.parse(decodeURIComponent(location.hash.slice(1)));
      if(typeof h.q==='string')s.q=h.q;if(h.tab&&KEY_BY_REPO[h.tab])s.repo=KEY_BY_REPO[h.tab];
      if(h.lic==='cc0')s.lic='cc0';if(typeof h.author==='string')s.author=h.author;if(h.sort==='name')s.sort='name'}catch(e){}
  }
  return s}
function pushURL(){
  var q=toParams(state).toString(),u=location.pathname+(q?'?'+q:'');
  try{history.replaceState(null,'',u)}catch(e){}}

/* ---------- card ---------- */
function resolveMedia(r,p){
  if(!p)return '';if(/^https?:\/\//i.test(p))return p;
  if(p.indexOf('releases/')===0)return 'https://github.com/'+OWNER+'/'+r.repo+'/'+p;
  return 'https://raw.githubusercontent.com/'+OWNER+'/'+r.repo+'/main/'+p}
function isAudio(p){return /\.(ogg|mp3|wav|flac)(\?|$)/i.test(p||'')}
function imgOf(r){return r.preview&&!isAudio(r.preview)?safeUrl(resolveMedia(r,r.preview)):''}
function audioOf(r){var s=r.sample||(isAudio(r.preview)?resolveMedia(r,r.preview):'');return safeUrl(s)}
function isPx(r){return r.repo==='assets-2d-pixel'||r.repo==='assets-ui-icons'}
function licShort(r){var l=(r.license||'').split(' (')[0].trim();return l.length>26?l.slice(0,25)+'…':l}
function licTitle(r){return (r.license||'')+(r.license_note?' — '+r.license_note:'')}
function licCredit(r){
  var l=r.license||'',m=/,\s*([^,()]+?)\s*선택\)?\s*$/.exec(l);
  if(m)return m[1];
  var s=l.split(' (')[0].trim();return s||l}
function creditLine(r){
  var t='"'+r.name+'" by '+(r.author||'Unknown');
  if(r.source_url)t+=' — '+r.source_url;
  t+=' — '+licCredit(r);
  if(!r.attribution_required)t+=' (표기 선택)';
  return t}
function shareURL(r){
  var p=new URLSearchParams();p.set('q',r.name);
  if((nameCount[(r.name||'').toLowerCase()]||0)>1&&KEY_BY_REPO[r.repo])p.set('repo',KEY_BY_REPO[r.repo]);
  return location.origin+location.pathname+'?'+p.toString()}
function partLabel(u){var n=decodeURIComponent(u.replace(/[?#].*$/,'').split('/').pop());
  if(/\.zip$/i.test(n)&&!/part\d/i.test(n))return n+' (마지막 조각)';return n}
function dlHtml(r){
  var u=r.download_urls;
  if(u.length>1)return '<details class="parts"><summary>다운로드 · 분할 파일 '+u.length+'개</summary><p class="hint">모두 같은 폴더에 받은 뒤 합쳐야 합니다. 합치는 방법은 <a href="https://github.com/'+OWNER+'/'+esc(r.repo)+'#readme" target="_blank" rel="noopener">저장소 README</a>를 참고하세요.</p>'+u.map(function(x){return '<a href="'+esc(x)+'" target="_blank" rel="noopener">'+esc(partLabel(x))+'</a>'}).join('')+'</details>';
  var one=safeUrl(r.download_url)||u[0];
  return one?'<a class="act pri" href="'+esc(one)+'" target="_blank" rel="noopener" aria-label="'+esc(r.name)+' 다운로드">다운로드</a>':''}
function card(r){
  var img=imgOf(r),ph=(audioOf(r)||r.repo==='assets-audio')?'🔊':'🖼';
  var th=img?'<button type="button" class="thumb'+(isPx(r)?' px':'')+'" data-act="zoom" data-i="'+r._i+'" aria-label="'+esc(r.name)+' 미리보기 크게 보기"><img loading="lazy" decoding="async" alt="" src="'+esc(img)+'"></button>'
    :'<div class="thumb noimg"><span class="ph" aria-hidden="true">'+ph+'</span></div>';
  var b='<span class="badge gray">'+esc(r._cat||r.type||'')+'</span>'
    +'<span class="badge'+(r.license_family==='cc0'?'':' by')+'" title="'+esc(licTitle(r))+'">'+esc(licShort(r))+'</span>'
    +(r.attribution_required?'<span class="badge by">표기 필요</span>':'<span class="badge">표기 불필요</span>')
    +(r.ai_generated?'<span class="badge ai">AI 생성</span>':'')
    +(r.download_urls.length>1?'<span class="badge by">분할 파일</span>':'');
  var tags=r.tags.slice(0,5).map(function(t){return '<span class="badge gray">'+esc(t)+'</span>'}).join('');
  var src=safeUrl(r.source_url);
  return '<article class="card">'+th+'<div class="meta"><h3 class="name">'+esc(r.name)+'</h3><div class="line">'+esc(r.type)+' · '+esc(SHORT[r.repo]||'')+' · '+esc(r.author)+'</div>'
    +'<div class="badges">'+b+'</div>'+(tags?'<div class="tags">'+tags+'</div>':'')
    +'<div class="line">추가 '+esc(r.added)+'</div>'
    +'<div class="acts">'+dlHtml(r)+(src?'<a class="act" href="'+esc(src)+'" target="_blank" rel="noopener" aria-label="'+esc(r.name)+' 원본 출처">출처</a>':'')+'</div>'
    +'<div class="acts"><button type="button" class="act" data-act="credit" data-i="'+r._i+'">크레딧 복사</button><button type="button" class="act" data-act="link" data-i="'+r._i+'">링크 복사</button><button type="button" class="act" data-act="detail" data-i="'+r._i+'" aria-expanded="false">상세</button></div>'
    +'<div class="det" hidden></div></div></article>'}
function detailHtml(r){
  var a=audioOf(r),rows=[];
  rows.push('<dt>라이선스</dt><dd>'+esc(r.license)+(r.license_note?'<br>'+esc(r.license_note):'')+'</dd>');
  if(r.attribution)rows.push('<dt>표기</dt><dd>'+esc(r.attribution)+'</dd>');
  if(r.notes)rows.push('<dt>구성</dt><dd>'+esc(r.notes)+'</dd>');
  if(r.effect_kind.length)rows.push('<dt>효과</dt><dd>'+esc(r.effect_kind.map(function(k){return FX_KO[k]?FX_KO[k]+'('+k+')':k}).join(', '))+'</dd>');
  rows.push('<dt>파일</dt><dd><code>'+esc(r.repo+'/'+(r.download_path||r.file))+'</code></dd>');
  if(r.tags.length>5)rows.push('<dt>태그</dt><dd>'+esc(r.tags.join(', '))+'</dd>');
  rows.push('<dt>저장소</dt><dd><a href="https://github.com/'+OWNER+'/'+esc(r.repo)+'" target="_blank" rel="noopener">'+esc(r.repo)+'</a></dd>');
  return '<dl>'+rows.join('')+'</dl>'+(a?'<audio controls preload="none" src="'+esc(a)+'"></audio>':'')}

/* ---------- render ---------- */
function activeItems(){
  var a=[];
  if(state.q)a.push(['d','검색 “'+state.q+'”']);
  if(state.repo)a.push(['d','저장소 '+(REPOS.filter(function(r){return r[0]===state.repo})[0]||[])[2]]);
  if(state.cat)a.push(['d','분류 '+CAT_LABEL[state.cat]]);
  if(state.lic)a.push(['d','라이선스 '+LIC_LABEL[state.lic]]);
  if(state.author)a.push(['d','제작자 '+state.author]);
  state.fx.forEach(function(k){a.push(['d','효과 '+FX.filter(function(f){return f[0]===k})[0][1]])});
  if(state.noattr)a.push(['d','표기 필요 없는 것만']);
  if(state.noai)a.push(['d','AI 생성 제외']);
  if(state.sort!=='new')a.push(['d','정렬 '+(state.sort==='name'?'이름':'종류')]);
  return a}
function syncControls(){
  $('q').value=state.q;$('cat').value=state.cat;$('lic').value=state.lic;$('author').value=state.author;$('sort').value=state.sort;
  $('noattr').checked=state.noattr;$('noai').checked=state.noai;
  [].forEach.call($('tabs').children,function(b){b.setAttribute('aria-pressed',String(b.getAttribute('data-t')===state.repo))});
  [].forEach.call($('chips').children,function(b){b.setAttribute('aria-pressed',String(state.fx.indexOf(b.getAttribute('data-fx'))>=0))});
}
function render(){
  list=filtered();shown=0;
  syncControls();pushURL();
  var act=activeItems();
  $('active').hidden=!act.length;
  $('active').innerHTML=act.length?'조건: '+act.map(function(x){return '<span>'+esc(x[1])+'</span>'}).join(''):'';
  $('reset').hidden=!act.length;
  var n=act.filter(function(x){return !/^(검색|저장소|효과)/.test(x[1])}).length;
  $('moreN').textContent=n?String(n):'';
  if(n)$('more').open=true;
  $('grid').innerHTML='';
  $('empty').hidden=list.length>0;
  $('count').textContent=fmt(list.length)+'개 / 전체 '+fmt(all.length)+'개';
  more();
  var port=state.repo==='portrait';$('people').hidden=!port;if(port)renderPeople();
}
function more(){
  var end=Math.min(shown+PAGE,list.length);
  if(end>shown){$('grid').insertAdjacentHTML('beforeend',list.slice(shown,end).map(card).join(''))}
  shown=end;
  var b=$('more-btn');b.hidden=shown>=list.length;
  b.textContent='더 보기 (남은 '+fmt(list.length-shown)+'개)';
  if(list.length)$('count').textContent=fmt(list.length)+'개 중 '+fmt(shown)+'개 표시 · 전체 '+fmt(all.length)+'개';
}

/* ---------- init ---------- */
function init(){
  $('loading').hidden=true;document.body.removeAttribute('aria-busy');
  var cnt={},cat={},lic={},au={},last='';
  all.forEach(function(r){cnt[r.repo]=(cnt[r.repo]||0)+1;cat[r.category]=(cat[r.category]||0)+1;lic[r.license_family]=(lic[r.license_family]||0)+1;if(r.author)au[r.author]=(au[r.author]||0)+1;if(r.added>last)last=r.added});
  $('sub').textContent='에셋 '+fmt(all.length)+'개'+REPOS.filter(function(r){return r[1]&&cnt[r[1]]}).map(function(r){return ' · '+SHORT[r[1]]+' '+fmt(cnt[r[1]])}).join('')+(last?' · 최근 추가 '+last:'');
  $('tabs').innerHTML=REPOS.map(function(t){var n=t[1]?(cnt[t[1]]||0):all.length;return '<button type="button" data-t="'+t[0]+'" aria-pressed="false">'+esc(t[2])+' '+fmt(n)+'</button>'}).join('');
  $('cat').innerHTML='<option value="">전체</option>'+CAT_ORDER.concat(Object.keys(cat).filter(function(k){return CAT_ORDER.indexOf(k)<0})).filter(function(k){return cat[k]}).map(function(k){return '<option value="'+esc(k)+'">'+esc(CAT_LABEL[k]||k)+' ('+fmt(cat[k])+')</option>'}).join('');
  $('lic').innerHTML='<option value="">전체</option>'+LIC_ORDER.filter(function(k){return lic[k]}).map(function(k){return '<option value="'+k+'">'+LIC_LABEL[k]+' ('+fmt(lic[k])+')</option>'}).join('');
  var col=new Intl.Collator('ko',{numeric:true,sensitivity:'base'});
  $('author').innerHTML='<option value="">전체</option>'+Object.keys(au).sort(col.compare).map(function(a){return '<option value="'+esc(a)+'">'+esc(a)+' ('+au[a]+')</option>'}).join('');
  $('chips').innerHTML=FX.map(function(f){return '<button type="button" data-fx="'+f[0]+'" aria-pressed="false">'+esc(f[1])+'</button>'}).join('');
  state=fromURL();
  if(state.author&&!au[state.author])state.author='';
    if(usedCsv){$('warn').innerHTML='<div class="warnbox">assets-index.min.json을 불러오지 못해 catalog.csv로 대신 표시합니다. 분류·효과 필터는 일부만 동작할 수 있습니다.</div>'}
  render();
}

/* ---------- copy ---------- */
var toastT;
function toast(m){var t=$('toast');t.textContent=m;t.classList.add('on');clearTimeout(toastT);toastT=setTimeout(function(){t.classList.remove('on')},1800)}
function copyText(t){
  if(navigator.clipboard&&navigator.clipboard.writeText&&window.isSecureContext)return navigator.clipboard.writeText(t).catch(function(){return legacyCopy(t)});
  return legacyCopy(t)}
function legacyCopy(t){return new Promise(function(res,rej){
  var a=document.createElement('textarea');a.value=t;a.setAttribute('readonly','');a.style.cssText='position:fixed;top:0;left:0;opacity:0';
  document.body.appendChild(a);a.select();var ok=false;try{ok=document.execCommand('copy')}catch(e){}
  document.body.removeChild(a);ok?res():rej(new Error('copy failed'))})}
function flash(btn,msg){
  var old=btn.getAttribute('data-old')||btn.textContent;btn.setAttribute('data-old',old);
  btn.textContent='복사됨 ✓';btn.classList.add('done');toast(msg);
  clearTimeout(btn._t);btn._t=setTimeout(function(){btn.textContent=old;btn.classList.remove('done');btn.removeAttribute('data-old')},1600)}

/* ---------- events ---------- */
var deb;
$('q').addEventListener('input',function(e){var v=e.target.value;clearTimeout(deb);deb=setTimeout(function(){state.q=v;render()},200)});
$('q').addEventListener('keydown',function(e){if(e.key==='Enter'){clearTimeout(deb);state.q=e.target.value;render()}});
$('cat').addEventListener('change',function(e){state.cat=e.target.value;render()});
$('lic').addEventListener('change',function(e){state.lic=e.target.value;render()});
$('author').addEventListener('change',function(e){state.author=e.target.value;render()});
$('sort').addEventListener('change',function(e){state.sort=e.target.value;render()});
$('noattr').addEventListener('change',function(e){state.noattr=e.target.checked;render()});
$('noai').addEventListener('change',function(e){state.noai=e.target.checked;render()});
$('reset').addEventListener('click',function(){clearTimeout(deb);state=clone(DEF);render();$('q').focus()});
$('more-btn').addEventListener('click',more);
$('tabs').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;state.repo=b.getAttribute('data-t');render()});
$('chips').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;var k=b.getAttribute('data-fx'),i=state.fx.indexOf(k);if(i>=0)state.fx.splice(i,1);else state.fx.push(k);render()});
$('grid').addEventListener('click',function(e){
  var b=e.target.closest('button[data-act]');if(!b)return;
  var r=all[+b.getAttribute('data-i')],act=b.getAttribute('data-act');if(!r)return;
  if(act==='credit')copyText(creditLine(r)).then(function(){flash(b,'크레딧을 복사했습니다')},function(){toast('복사하지 못했습니다')});
  else if(act==='link')copyText(shareURL(r)).then(function(){flash(b,'링크를 복사했습니다')},function(){toast('복사하지 못했습니다')});
  else if(act==='detail'){
    var d=b.closest('.card').querySelector('.det'),open=b.getAttribute('aria-expanded')!=='true';
    if(open&&!d.innerHTML)d.innerHTML=detailHtml(r);
    d.hidden=!open;b.setAttribute('aria-expanded',String(open))}
  else if(act==='zoom'){
    var im=imgOf(r);
    $('dlgbody').innerHTML='<div class="dhead"><div class="dimg"><img class="'+(isPx(r)?'px':'')+'" alt="'+esc(r.name)+' 미리보기" src="'+esc(im)+'"></div><button type="button" class="close" aria-label="닫기">✕</button></div><div class="dcap">'+esc(r.name)+'</div>';
    var dg=$('dlg');if(dg.showModal)dg.showModal();else dg.setAttribute('open','')}
});
$('grid').addEventListener('error',function(e){
  var im=e.target;if(!im||im.tagName!=='IMG')return;
  var s=document.createElement('span');s.className='ph';s.setAttribute('aria-hidden','true');s.textContent='🖼';im.replaceWith(s)},true);
$('dlg').addEventListener('click',function(e){if(e.target===this||e.target.classList.contains('close'))this.close()});
window.addEventListener('popstate',function(){if(all.length){state=fromURL();render()}});

/* ---------- 초상화 인물 검색 ---------- */
var PIDX='https://raw.githubusercontent.com/sigco3111/assets-2d-portraits/main/people-index.json';
var PTHUMB='https://raw.githubusercontent.com/sigco3111/assets-2d-portraits/main/';
var people=null,ploading=false,pshown=PAGE;
function loadPeople(){if(people||ploading)return;ploading=true;
  fetch(PIDX).then(function(r){if(!r.ok)throw new Error(r.status);return r.json()}).then(function(d){people=d;renderPeople()}).catch(function(){ploading=false;$('phint').hidden=false;$('phint').textContent='인물 색인을 불러오지 못했습니다. 잠시 후 다시 시도하세요.'})}
function renderPeople(){
  if($('people').hidden)return;
  loadPeople();
  var q=($('pq').value||'').trim(),grid=$('pgrid'),cnt=$('pcount');
  if(!people){cnt.textContent='인물 색인 불러오는 중…';return}
  $('phint').hidden=true;
  var l=!q?people:q==='미정'?people.filter(function(p){return !p.name_ko}):people.filter(function(p){return (p.name_ko&&p.name_ko.indexOf(q)>=0)||(p.name_zh&&p.name_zh.indexOf(q)>=0)});
  var s=l.slice(0,pshown);
  grid.innerHTML=s.map(function(p){var nm=p.name_ko||'미정';return '<a class="pc" href="'+esc(safeUrl(p.dl))+'" target="_blank" rel="noopener" title="원본 다운로드"><img loading="lazy" decoding="async" alt="'+esc(nm)+'" src="'+PTHUMB+esc(p.thumb)+'"><div class="pn">'+esc(nm)+'</div><div class="pz">'+esc(p.name_zh)+'</div></a>'}).join('')+(l.length>pshown?'<button type="button" class="morebtn" id="pmore">더 보기 (남은 '+fmt(l.length-pshown)+'명)</button>':'');
  cnt.textContent=l.length?(fmt(l.length)+'명 · '+fmt(s.length)+'명 표시'):'검색 결과가 없습니다.';
  var m=$('pmore');if(m)m.onclick=function(){pshown+=PAGE;renderPeople()}}
$('pq').addEventListener('input',function(){pshown=PAGE;renderPeople()});

load();
})();
