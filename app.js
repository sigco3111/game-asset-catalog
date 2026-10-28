(function(){
'use strict';
var OWNER='sigco3111';
var TABS=[['','전체'],['assets-2d-pixel','2D·텍스처'],['assets-3d-lowpoly','3D'],['assets-ui-icons','UI·아이콘'],['assets-audio','오디오']];
var KIND={'assets-2d-pixel':'2D','assets-3d-lowpoly':'3D','assets-ui-icons':'UI','assets-audio':'오디오'};
var SYN={'던전':['dungeon'],'나무':['tree','nature','forest'],'숲':['forest','nature'],'칼':['sword','weapon'],'검':['sword','weapon'],'무기':['weapon'],'총':['gun','shooter','blaster'],'캐릭터':['character'],'몬스터':['monster','creature','zombie'],'적':['enemy'],'도시':['city','town','urban'],'마을':['town','village'],'집':['house','building'],'건물':['building'],'자동차':['car','vehicle','racing'],'탈것':['vehicle'],'우주':['space','scifi'],'로봇':['robot'],'음식':['food'],'농작물':['crops','farm'],'효과음':['sfx','sound'],'음악':['music'],'아이콘':['icon','icons'],'버튼':['button','ui'],'배경':['background'],'타일':['tile','tileset'],'퍼즐':['puzzle'],'픽셀':['pixel'],'물고기':['fish'],'동물':['animal','animals'],'배':['ship','boat'],'비행기':['plane','aircraft'],'해적':['pirate'],'좀비':['zombie'],'판타지':['fantasy'],'중세':['medieval'],'폭발':['explosion','particle'],'이펙트':['effect','effects','particles'],'음성':['voice'],'인터페이스':['interface','ui']};
var rows=[],state={q:'',tab:'',lic:'',author:'',sort:'new'};
var $=function(id){return document.getElementById(id)};

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
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function isBy(r){return /BY/i.test(r.license)}
function parts(r){var u=dl(r);if(!r.split||!u)return [];var b=u.replace(/[^\/]*$/,'');return r.split.split(';').map(function(x){return x.trim()}).filter(Boolean).map(function(x){return {n:x,u:b+x}})}
function dl(r){var f=r.file;if(!f)return '';if(/^https?:/.test(f))return f;
  return 'https://github.com/'+OWNER+'/'+r.repo+(f.indexOf('releases/')===0?'/'+f:'/raw/main/'+f)}
function repoUrl(r){return 'https://github.com/'+OWNER+'/'+r.repo}
function problems(r){var p=[];
  if(!r.name)p.push('이름');if(!r.file)p.push('파일');if(!r.license)p.push('라이선스');
  if(!r.source_url)p.push('출처');
  if(r.repo!=='assets-audio'&&!r.preview)p.push('미리보기');
  return p}
function cleanNotes(n){
  return n.split(';').map(function(s){return s.trim()}).filter(Boolean).map(function(s){
    if(/^\{.*\}$/.test(s)){var parts=[],re=/'\.(\w+)':\s*(\d+)/g,m;while((m=re.exec(s)))parts.push(m[1].toUpperCase()+' '+m[2]+'개');return parts.join(', ')}
    return s}).filter(function(s){return !/^샘플:|^미러 바이트|공식 GitHub 바이트$|^릴리스 v[\d.]+ 첨부$/.test(s)}).join(' · ');
}
function mirror(r){return /미러 바이트/.test(r.notes)}
function search(r){return (r.name+' '+r.tags+' '+r.author+' '+r.type+' '+r.notes+' '+(KIND[r.repo]||'')).toLowerCase()}
function filtered(){
  var terms=state.q.toLowerCase().split(/\s+/).filter(Boolean);
  var list=rows.filter(function(r){
    if(state.tab&&r.repo!==state.tab)return false;
    if(state.lic==='cc0'&&isBy(r))return false;
    if(state.lic==='by'&&!isBy(r))return false;
    if(state.author&&r.author!==state.author)return false;
    var s=r._s;for(var i=0;i<terms.length;i++){var alts=[terms[i]].concat(SYN[terms[i]]||[]);if(!alts.some(function(a){return s.indexOf(a)>=0}))return false}
    return true});
  if(state.sort==='name')list.sort(function(a,b){return a.name.localeCompare(b.name,'ko')});
  else list.sort(function(a,b){return (b.added||'').localeCompare(a.added||'')||b._i-a._i});
  return list}
function card(r){
  var px=r.repo==='assets-2d-pixel'||r.repo==='assets-ui-icons';
  var th=r.preview?'<img loading="lazy" decoding="async" alt="" src="'+esc(r.preview)+'" onerror="this.replaceWith(Object.assign(document.createElement(\'span\'),{className:\'ph\',textContent:\'🖼\'}))">':'<span class="ph">'+(r.repo==='assets-audio'?'🔊':'🖼')+'</span>';
  var b='<span class="badge gray">'+esc(KIND[r.repo]||'')+'</span>'+(isBy(r)?'<span class="badge by">귀속 필요</span>':'<span class="badge">CC0</span>');
  if(r.split)b+='<span class="badge by">분할 ZIP</span>';
  if(problems(r).length)b+='<span class="badge chk">확인 필요</span>';
  return '<button class="card" data-i="'+r._i+'"><div class="thumb'+(px?' px':'')+'">'+th+'</div><div class="meta"><div class="name">'+esc(r.name)+'</div><div class="line">'+esc(r.type)+' · '+esc(r.author)+'</div><div class="badges">'+b+'</div></div></button>'}
function render(){
  var l=filtered();
  $('grid').innerHTML=l.map(card).join('');
  $('empty').hidden=l.length>0;
  $('count').textContent=l.length+'팩 / 전체 '+rows.length+'팩';
  var tabs=TABS.map(function(t){var n=rows.filter(function(r){return !t[0]||r.repo===t[0]}).length;
    return '<button type="button" data-t="'+t[0]+'" aria-pressed="'+(state.tab===t[0])+'">'+t[1]+' '+n+'</button>'}).join('');
  $('tabs').innerHTML=tabs;
  var bad=rows.filter(function(r){return problems(r).length});
  $('warn').innerHTML=(state.lic!=='cc0'&&rows.some(isBy))?'<div class="warnbox">귀속 필요 표시가 있는 팩(예: Game-icons.net)은 게임에 쓸 때 제작자 표기가 필요합니다. 팩 상세에서 귀속 문구를 확인하세요.'+(bad.length?' · 기록이 빠진 팩 '+bad.length+'개는 "확인 필요"로 표시됩니다.':'')+'</div>':(bad.length?'<div class="warnbox">기록이 빠진 팩 '+bad.length+'개는 "확인 필요"로 표시됩니다.</div>':'');
  var h='#'+encodeURIComponent(JSON.stringify(state));try{history.replaceState(null,'',h==='#%7B%22q%22%3A%22%22%2C%22tab%22%3A%22%22%2C%22lic%22%3A%22%22%2C%22author%22%3A%22%22%2C%22sort%22%3A%22new%22%7D'?location.pathname+location.search:h)}catch(e){}
}
function detail(r){
  var px=r.repo==='assets-2d-pixel'||r.repo==='assets-ui-icons',p=problems(r),n=[];
  if(isBy(r))n.push('<div class="notice w"><b>귀속 필요.</b> '+esc(r.attribution||'귀속 문구를 원본 license.txt에서 확인하세요.')+'<br>라이선스: '+esc(r.license)+'</div>');
  if(r.split)n.push('<div class="notice w"><b>분할 ZIP.</b> 아래 조각 '+parts(r).length+'개를 모두 같은 폴더에 받은 뒤 합쳐야 합니다. 합치는 방법은 <a href="'+repoUrl(r)+'#readme" target="_blank" rel="noopener">저장소 README</a>를 참고하세요.</div>');
  if(mirror(r))n.push('<div class="notice n">파일은 공식 미러에서 받았고 공식 사이트 원본과 바이트 대조는 하지 않았습니다. 라이선스는 원본 배포 페이지와 동봉 License.txt를 확인했습니다.</div>');
  if(p.length)n.push('<div class="notice w"><b>확인 필요.</b> 카탈로그에 빠진 항목: '+esc(p.join(', '))+'</div>');
  var img=r.preview?'<img class="'+(px?'px':'')+'" alt="'+esc(r.name)+' 미리보기" src="'+esc(r.preview)+'">':'<span class="ph" style="font-size:48px">'+(r.repo==='assets-audio'?'🔊':'🖼')+'</span>';
  var tags=r.tags?r.tags.split(',').map(function(t){return '<span class="badge gray">'+esc(t.trim())+'</span>'}).join(' '):'';
  var h='<div class="dhead"><div class="dimg">'+img+'</div><button class="close" aria-label="닫기">✕</button></div><div class="dbody"><h2>'+esc(r.name)+'</h2><div class="line">'+esc(r.type)+' · '+esc(KIND[r.repo]||'')+'</div>'+n.join('')+
   '<dl><dt>제작자</dt><dd>'+esc(r.author)+'</dd><dt>라이선스</dt><dd>'+esc(r.license)+'</dd><dt>구성</dt><dd>'+esc(cleanNotes(r.notes))+'</dd><dt>태그</dt><dd>'+tags+'</dd><dt>추가일</dt><dd>'+esc(r.added)+'</dd></dl>'+
   (r.sample?'<audio controls preload="none" src="'+esc(r.sample)+'"></audio>':'')+'<div style="margin-top:10px">'+
   (r.file&&!r.split?'<a class="btn" href="'+esc(dl(r))+'" target="_blank" rel="noopener">다운로드</a>':'')+parts(r).map(function(p,i,a){return '<a class="btn'+(i?' sec':'')+'" href="'+esc(p.u)+'" target="_blank" rel="noopener">'+(/\.zip$/.test(p.n)?'.zip (마지막 조각)':p.n.replace(/^.*(\.z\d+)$/,'$1 조각'))+'</a>'}).join('')+
   (r.source_url?'<a class="btn sec" href="'+esc(r.source_url)+'" target="_blank" rel="noopener">원본 출처</a>':'')+
   '<a class="btn sec" href="'+repoUrl(r)+'" target="_blank" rel="noopener">저장소</a></div></div>';
  $('dlgbody').innerHTML=h;var d=$('dlg');if(d.showModal)d.showModal();else d.setAttribute('open','')}
function init(data){
  rows=parseCSV(data).filter(function(r){return r.name||r.file});
  rows.forEach(function(r,i){r._i=i;r._s=search(r)});
  var by={};rows.forEach(function(r){if(r.author)by[r.author]=(by[r.author]||0)+1});
  $('author').innerHTML='<option value="">제작자</option>'+Object.keys(by).sort(function(a,b){return by[b]-by[a]}).map(function(a){return '<option value="'+esc(a)+'">'+esc(a)+' ('+by[a]+')</option>'}).join('');
  try{var s=JSON.parse(decodeURIComponent(location.hash.slice(1)));for(var k in state)if(typeof s[k]==='string')state[k]=s[k]}catch(e){}
  $('q').value=state.q;$('lic').value=state.lic;$('author').value=state.author;$('sort').value=state.sort;
  var last=rows.map(function(r){return r.added}).sort().pop();
  $('sub').textContent='에셋 팩 '+rows.length+'개'+(last?' · 최근 추가 '+last:'')+' · 한국어 검색';
  render()}
$('q').addEventListener('input',function(e){state.q=e.target.value;render()});
$('lic').addEventListener('change',function(e){state.lic=e.target.value;render()});
$('author').addEventListener('change',function(e){state.author=e.target.value;render()});
$('sort').addEventListener('change',function(e){state.sort=e.target.value;render()});
$('reset').addEventListener('click',function(){state={q:'',tab:'',lic:'',author:'',sort:'new'};$('q').value='';$('lic').value='';$('author').value='';$('sort').value='new';render()});
$('tabs').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;state.tab=b.getAttribute('data-t');render()});
$('grid').addEventListener('click',function(e){var b=e.target.closest('.card');if(!b)return;detail(rows[+b.getAttribute('data-i')])});
$('dlg').addEventListener('click',function(e){if(e.target===this||e.target.classList.contains('close')){this.close();var a=this.querySelector('audio');if(a)a.pause()}});
fetch('catalog.csv',{cache:'no-cache'}).then(function(r){if(!r.ok)throw new Error(r.status);return r.text()}).then(init).catch(function(e){$('sub').textContent='카탈로그를 불러오지 못했습니다. 잠시 후 다시 시도하세요.';console.error(e)});
})();
