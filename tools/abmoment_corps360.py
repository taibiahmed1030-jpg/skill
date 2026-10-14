import onnxruntime as ort, numpy as np, cv2
from PIL import Image, ImageFilter
sess=ort.InferenceSession('esrgan_x4.onnx', providers=['CPUExecutionProvider'])
def up(a):
    x=(a.astype(np.float32)/255.).transpose(2,0,1)[None]
    y=sess.run(None,{'input':x})[0][0].transpose(1,2,0)
    return (np.clip(y,0,1)*255).round().astype(np.uint8)
src=np.asarray(Image.open('/root/.claude/uploads/9b15bc7c-0dd1-5dc9-8e9a-f5b48a131f45/228f15d4-image.jpg').convert('RGB'))
bg=np.array([244,243,238]); PAGE=np.array([247,246,243])
runs=[(27,228),(256,436),(471,566),(602,776),(806,1006)]
W=240  # largeur de cadre en px source
H=src.shape[0]
views=[]
for x0,x1 in runs:
    d=np.sqrt(((src.astype(int)-bg)**2).sum(-1))>30
    sub=d[120:300,x0:x1]; ys,xs=np.nonzero(sub); cx=x0+xs.mean()
    l=int(round(cx-W/2)); fr=np.full((H,W,3),bg,np.uint8)
    a,b=max(l,0),min(l+W,src.shape[1]); 
    # ne garder que la figure courante (masquer les voisines)
    piece=src[:,a:b].copy(); m=np.zeros(piece.shape[:2],bool); m[:, max(x0-6,a)-a:min(x1+6,b)-a]=True
    piece[~m]=bg
    fr[:,a-l:b-l]=piece
    views.append(fr)
ups=[up(v) for v in views]
print('upscaled', ups[0].shape)
OW,OH=600,1430
def fin(a):
    a=cv2.resize(a,(OW,OH),interpolation=cv2.INTER_AREA).astype(np.float32)
    a=a*(PAGE/bg)
    lum=a.mean(-1); sat=a.max(-1)-a.min(-1)
    w=np.clip((lum-234)/8,0,1)*np.clip((14-sat)/6,0,1)
    a=a*(1-w[...,None])+PAGE*w[...,None]
    return np.clip(a,0,255).astype(np.uint8)
base=[fin(u) for u in ups]
key=base+[base[3][:,::-1].copy(),base[2][:,::-1].copy(),base[1][:,::-1].copy()]
dis=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
def flow(a,b):
    ga=cv2.cvtColor(a,cv2.COLOR_RGB2GRAY); gb=cv2.cvtColor(b,cv2.COLOR_RGB2GRAY)
    return dis.calc(ga,gb,None)
gy,gx=np.mgrid[0:OH,0:OW].astype(np.float32)
N=4  # images par segment de 45°
frames=[]
for i in range(8):
    A=key[i]; B=key[(i+1)%8]
    fab=flow(A,B); fba=flow(B,A)
    for k in range(N):
        t=k/N
        if t==0: frames.append(A); continue
        wa=cv2.remap(A,gx+t*fba[...,0],gy+t*fba[...,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
        wb=cv2.remap(B,gx+(1-t)*fab[...,0],gy+(1-t)*fab[...,1],cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
        w={0.25:0.06,0.5:0.3,0.75:0.92}[t]
        fa=wa.astype(np.float32); fb=wb.astype(np.float32)
        diff=np.abs(fa-fb).mean(-1); hard=np.clip((diff-18)/22,0,1)
        hard=cv2.GaussianBlur(hard,(0,0),3)[...,None]
        sel=float(w>0.5)
        ww=(1-hard)*w+hard*sel
        frames.append(((1-ww)*fa+ww*fb).astype(np.uint8))
import os
O='/home/user/skill/abmoment/assets/img/corps-360/'; os.makedirs(O,exist_ok=True)
for f in os.listdir(O): os.remove(O+f)
for i,f in enumerate(frames): Image.fromarray(f).save(f'{O}{i:02d}.webp',quality=80,method=6)
sheet=Image.new('RGB',(OW//4*16,OH//4*2))
for i,f in enumerate(frames): sheet.paste(Image.fromarray(f).resize((OW//4,OH//4)),((i%16)*OW//4,(i//16)*OH//4))
sheet.save('turn/sheet.jpg',quality=85); print(len(frames))
