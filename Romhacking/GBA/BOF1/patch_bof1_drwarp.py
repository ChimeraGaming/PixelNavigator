import argparse, hashlib, pathlib, struct

class Thumb:
 def __init__(self, base): self.base=base; self.data=bytearray(); self.labels={}; self.fix=[]; self.pool=[]
 def h(self,x): self.data+=struct.pack('<H',x)
 def label(self,n): self.labels[n]=self.base+len(self.data)
 def lit(self,r,v): self.fix.append(('lit',len(self.data),r,v)); self.h(0)
 def mov(self,r,v): self.h(0x2000|r<<8|v)
 def cmp(self,r,v): self.h(0x2800|r<<8|v)
 def mem(self,op,r,b,o=0):
  codes={'ldr':(0x6800,4),'str':(0x6000,4),'ldrh':(0x8800,2),'strh':(0x8000,2),'ldrb':(0x7800,1),'strb':(0x7000,1)}
  c,s=codes[op]; assert o%s==0 and o//s<32; self.h(c|(o//s)<<6|b<<3|r)
 def add(self,r,v): self.h(0x3000|r<<8|v)
 def branch(self,n,cond=None): self.fix.append(('branch',len(self.data),cond,n)); self.h(0)
 def bl(self,address):
  d=address-(self.base+len(self.data)+4); assert -0x400000<=d<0x400000 and d%2==0
  self.h(0xf000|((d>>12)&0x7ff)); self.h(0xf800|((d>>1)&0x7ff))
 def finish(self):
  while len(self.data)%4:self.h(0x46c0)
  for kind,o,r,v in self.fix:
   if kind=='lit':
    p=self.base+len(self.data); self.data+=struct.pack('<I',v); d=p-((self.base+o+4)&~3); assert 0<=d<=1020; x=0x4800|r<<8|d//4
   else:
    d=(self.labels[v]-(self.base+o+4))//2
    if r is None: assert -1024<=d<1024; x=0xe000|(d&0x7ff)
    else: assert -128<=d<128; x=0xd000|r<<8|(d&255)
   struct.pack_into('<H',self.data,o,x)
  return self.data

SOURCE_SHA256 = "3289aec193497c86c3c769b42c1024a1d491d48f15b90fcb58910dca0a79647a"

def patch(source):
 BASE=0x083fe000; MAIL=0x0203ffa0; MAGIC=0x44525750
 t=Thumb(BASE); t.h(0xb5ff)
 t.lit(4,MAIL); t.mem('ldr',0,4); t.lit(1,MAGIC); t.h(0x4288); t.branch('done',1)
 t.mem('ldrb',0,4,15);t.cmp(0,1);t.branch('warpcheck',1)
 t.mem('ldrb',0,4,4); t.cmp(0,1); t.branch('warpcheck',1)
 t.mov(0,0);t.mem('strb',0,4,4)
 t.bl(0x0805d8f4);t.h(0x1c07);t.lit(5,0x0202ddd4);t.mov(6,0);t.mov(2,0)
 t.label('scan');t.mem('ldrh',0,5);t.h(0x0601);t.h(0x0e09);t.cmp(1,0x36);t.branch('exists',0)
 t.lit(1,0xf00);t.h(0x4008);t.cmp(0,0);t.branch('next',1);t.cmp(2,0);t.branch('next',1);t.h(0x1c2a)
 t.label('next');t.add(5,2);t.add(6,1);t.h(0x42be);t.branch('scan',3)
 t.cmp(2,0);t.branch('full',0);t.lit(0,0x136);t.mem('strh',0,2);t.mov(0,1);t.branch('status')
 t.label('exists');t.mov(0,2);t.branch('status')
 t.label('full');t.mov(0,3)
 t.label('status');t.mem('strb',0,4,6)
 t.label('warpcheck');t.mem('ldrb',0,4,5);t.cmp(0,1);t.branch('outgoing',0);t.cmp(0,2);t.branch('done',1)
 t.mem('ldrb',0,4,7);t.cmp(0,1);t.branch('done',1)
 t.mem('ldrh',5,4,8);t.mem('ldrh',6,4,10);t.mem('ldrh',7,4,12);t.mov(0,0);t.mem('strb',0,4,7);t.branch('travel')
 t.label('outgoing');t.mem('ldrb',0,4,7);t.cmp(0,0);t.branch('done',1)
 t.mem('ldrb',0,4,15);t.cmp(0,1);t.branch('done',1)
 t.mem('ldrh',0,4,20);t.lit(1,496);t.h(0x4288);t.branch('done',2)
 t.lit(0,0x03002484);t.mem('ldrh',1,0);t.mem('strh',1,4,8)
 t.lit(0,0x03002ab0);t.mem('ldrh',1,0,2);t.mem('strh',1,4,10);t.mem('ldrh',1,0,6);t.mem('strh',1,4,12)
 t.lit(0,0x03002b11);t.mem('ldrb',1,0);t.mem('strb',1,4,14);t.mov(0,1);t.mem('strb',0,4,7)
 t.mem('ldrh',5,4,20);t.mem('ldrh',6,4,22);t.mem('ldrh',7,4,24)
 t.label('travel');t.mov(0,0);t.mem('strb',0,4,5)
 t.mov(0,16);t.mov(1,0);t.bl(0x0800312c);t.mov(0,16);t.bl(0x08000248)
 t.lit(0,0x03002484);t.mem('strh',5,0)
 t.lit(0,0x0202de54);t.mem('strh',5,0)
 t.lit(0,0x030045b0);t.mem('strh',5,0,8)
 t.lit(0,0x0202dbd0);t.mem('strh',6,0,6);t.mem('strh',7,0,10)
 t.lit(0,0x03002ab0);t.mem('strh',6,0,2);t.mem('strh',7,0,6)
 t.lit(0,0x030023d4);t.mem('strh',6,0);t.lit(0,0x030040e0);t.mem('strh',7,0)
 t.bl(0x08029094);t.bl(0x080028b0);t.h(0x1c28);t.bl(0x0803ad54)
 t.mov(0,16);t.mov(1,2);t.bl(0x0800312c)
 t.label('done');t.bl(0x08003218);t.h(0xbcff);t.h(0xbc08);t.h(0x4718)
 code=t.finish()
 h=Thumb(BASE+0x400);h.h(0xb510);h.lit(4,MAIL);h.mem('ldr',0,4);h.lit(1,MAGIC);h.h(0x4288);h.branch('disabled',1)
 h.mem('ldrb',0,4,15);h.cmp(0,1);h.branch('disabled',1)
 h.mov(0,1);h.mem('strb',0,4,17);h.branch('exit')
 h.label('disabled');h.mov(0,12);h.lit(1,0x03004620);h.mem('strb',0,1,3);h.mov(0,0);h.mem('strb',0,1,7)
 h.label('exit');h.h(0xbc10);h.h(0xbc08);h.h(0x4718)
 rom=bytearray(source);rom[0x3fe000:0x3fe000+len(code)]=code;handler=h.finish();rom[0x3fe400:0x3fe400+len(handler)]=handler
 for offset in (0x156a,0x164c):
  hook=Thumb(0x08000000+offset);hook.bl(BASE);rom[offset:offset+4]=hook.data
 struct.pack_into('<I',rom,0x150908,BASE+0x401)
 rom[0x22007c+0x36*14+8]=0x50
 rom[0x3fe800:0x3fe810]=b'PNDW044ABFE0002\x00'
 return bytes(rom)

def ips(source, target):
 out=bytearray(b'PATCH');at=0
 while at<len(source):
  if source[at]==target[at]: at+=1;continue
  begin=at
  while at<len(source) and source[at]!=target[at] and at-begin<65535: at+=1
  out+=begin.to_bytes(3,'big')+(at-begin).to_bytes(2,'big')+target[begin:at]
 return bytes(out+b'EOF')

def main():
 parser=argparse.ArgumentParser(description='Create a BOF1 USA GBA DrWarp copy for Pixel Navigator 0.4.4.')
 parser.add_argument('source',type=pathlib.Path)
 parser.add_argument('output',type=pathlib.Path)
 parser.add_argument('--ips',type=pathlib.Path)
 args=parser.parse_args()
 if args.source.resolve()==args.output.resolve() or args.output.exists(): parser.error('Choose a new output path; the source and existing files are preserved.')
 source=args.source.read_bytes()
 if hashlib.sha256(source).hexdigest()!=SOURCE_SHA256: parser.error('Unsupported ROM. Requires unmodified ABFE USA revision 0.')
 target=patch(source)
 with args.output.open('xb') as out:out.write(target)
 if args.ips:
  with args.ips.open('xb') as out:out.write(ips(source,target))
 print('Created',args.output,'SHA256',hashlib.sha256(target).hexdigest())

if __name__=='__main__': main()
