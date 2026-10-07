"""Read the native USA GBA map names and entry records for the DrWarp picker."""
import argparse, hashlib, json, pathlib, struct
SOURCE='3289aec193497c86c3c769b42c1024a1d491d48f15b90fcb58910dca0a79647a'
CINEMA={102:('Large face - muted palette',632,28796),103:('Large purple face',632,28796),104:('Breath of Fire title artwork',136,28796),395:('Stone guardian on a mountain',896,28796),396:('Blue-haired woman portrait',1160,28780),397:('Dragon artwork - scrambled scene',384,29564),398:('Sunset artwork - scrambled scene',1152,29052),399:('Stone guardian portrait',384,29052)}
def extract(rom):
 if hashlib.sha256(rom).hexdigest()!=SOURCE:raise ValueError('Requires unmodified ABFE USA revision 0')
 half=lambda at:struct.unpack_from('<H',rom,at)[0]
 def text(pointer):
  out=[]
  for value in rom[pointer:pointer+80]:
   if value==0:break
   if value==2:out.append(' ')
   elif 0x20<=value<=0x29:out.append(chr(48+value-0x20))
   elif 0x2a<=value<=0x43:out.append(chr(65+value-0x2a))
   elif 0x48<=value<=0x61:out.append(chr(97+value-0x48))
   elif value in (0xef,0xf0,0x67,0x46):out.append({0xef:'.',0xf0:'-',0x67:'&',0x46:'?'}[value])
   else:raise ValueError('Unknown map-name character '+hex(value))
  return ''.join(out)
 names=[text(struct.unpack_from('<I',rom,0x14f114+i*4)[0]-0x08000000) for i in range(64)]
 maps=[];incoming={i:[] for i in range(496)}
 for i in range(496):
  at=0x1ac308+half(0x1abb54+i*2);at+=rom[at]+1;count=rom[at];exits=[]
  for j in range(count):
   x,y,dx,dy,target,direction=struct.unpack_from('<5HB',rom,at+1+j*11)
   if target&0x7fff>=496:raise ValueError('Invalid exit destination')
   if not x&0x8000:
    exits.append({'x':x,'y':y,'map':target&0x7fff})
    point=[dx,dy]
    if direction==0:point[1]-=16
    elif direction==2:point[1]+=16
    elif direction==1:point[0]-=16
    elif direction==3:point[0]+=16
    if 0<=point[0]<=8191 and 0<=point[1]<=65535:incoming[target&0x7fff].append(point)
  fallback=struct.unpack_from('<3HB',rom,at+1+count*11)
  descriptor=rom[0xf92d4+i];index=rom[0x14bf54+i-1] if i else 0
  assert index<64
  native=names[index] if index else None
  kind={0:'World layout',1:'Field',2:'Interior',3:'Structure',4:'Cutscene'}[descriptor&7]
  title='World Map' if i==0 else native if native else kind+' - unnamed'
  if i in CINEMA:title='Cutscene - '+CINEMA[i][0]
  if i==390:title='Dragon Tmple - ruined exterior'
  if i==271:title='Dragon Tmple - linked interior'
  maps.append(dict(id=i,label=title,gameName=native,nameIndex=index,bank=descriptor>>4,type=descriptor&7,kind=kind,exits=exits,nativeSpawn=list(fallback),entry=None,entrySource=None,visualChecked=i in CINEMA or i in (390,271),unusedStatus='unverified'))
 for item in maps:
  i=item['id'];point=incoming[i][0] if incoming[i] else None;source='native incoming exit' if point else None
  if point is None:
   x,y,_,direction=item['nativeSpawn'];point=[x,y]
   if direction==0:point[1]-=16
   elif direction==2:point[1]+=16
   elif direction==1:point[0]-=16
   elif direction==3:point[0]+=16
   if not(0<=point[0]<=8191 and 0<=point[1]<=65535):point=None
   source='native spawn record' if point else None
  if i in CINEMA:point=list(CINEMA[i][1:]);source='live visual check'
  if i==390:point=[520,9244];source='live visual check'
  if i==271:point=[6008,36460];source='live visual check'
  item['entry']=point;item['entrySource']=source
 return dict(schema=1,game='breath_of_fire_gba',code='ABFE',revision=0,romSha256=SOURCE,source='Native menu routine 0x08062852, name-index table 0x0814bf54 and name pointers 0x0814f114',maps=maps)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('rom',type=pathlib.Path);p.add_argument('output',type=pathlib.Path);a=p.parse_args();catalog=extract(a.rom.read_bytes());a.output.write_text(json.dumps(catalog,indent=2)+'\n');print('Cataloged',len(catalog['maps']),'maps;',sum(m['gameName'] is not None for m in catalog['maps']),'native location names')
