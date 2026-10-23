"""Synthesise a light, upbeat 100 bpm bed for the tirgulim ad (no samples, no licences).
usage: python3 music.py out.wav [seconds]"""
import sys, wave, numpy as np
SR=48000; T=float(sys.argv[2]) if len(sys.argv)>2 else 27.8; N=int(SR*T); t=np.arange(N)/SR
BEAT=0.6; out=np.zeros((N,2))
nf=lambda m:440*2**((m-69)/12)
# C - G - Am - F, two bars each
CH=[[48,55,60,64,67],[43,50,55,59,62],[45,52,57,60,64],[41,48,53,57,60]]
def add(sig,start,pan=0.0,gain=1.0):
    i=int(start*SR); n=min(len(sig),N-i)
    if n<=0: return
    out[i:i+n,0]+=sig[:n]*gain*(1-pan)/1.0; out[i:i+n,1]+=sig[:n]*gain*(1+pan)/1.0
def tone(f,d,harm=(1,.5,.25),att=.01,dec=None):
    tt=np.arange(int(d*SR))/SR; s=sum(a*np.sin(2*np.pi*f*k*tt) for k,a in enumerate(harm,1))
    env=np.minimum(1,tt/att)*(np.exp(-tt/dec) if dec else np.minimum(1,(d-tt)/0.3))
    return s*env
bar=4*BEAT; seg=2*bar
k=0; s=0.0
while s<T:
    ch=CH[k%4]
    for m in ch:  # pad
        for det in (-0.08,0.08):
            add(tone(nf(m)*(1+det/100),seg,harm=(1,.35,.12),att=0.6),s,pan=det*4,gain=0.035)
    for b in range(8):  # bass on beats
        add(tone(nf(ch[0]-12),BEAT*0.9,harm=(1,.4,.1),att=.005,dec=.25),s+b*BEAT,gain=0.16 if s>=3 else 0.0)
    for e in range(16):  # pluck arpeggio in eighths
        m=ch[[2,3,4,3,1,3,4,2][e%8]]+12
        add(tone(nf(m),0.5,harm=(1,.6,.3,.15),att=.003,dec=.12),s+e*BEAT/2,pan=0.3*(-1)**e,gain=0.07 if s>=0.2 else 0)
    s+=seg; k+=1
# drums
def kick():
    tt=np.arange(int(0.35*SR))/SR; f=50+90*np.exp(-tt*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*9)
def hat():
    tt=np.arange(int(0.08*SR))/SR; n=np.random.default_rng(1).standard_normal(len(tt)); n=np.diff(n,prepend=0); return n*np.exp(-tt*60)
def clap():
    tt=np.arange(int(0.2*SR))/SR; n=np.random.default_rng(2).standard_normal(len(tt)); return n*np.exp(-tt*25)*0.6
b=0
while b*BEAT<T-1.2:
    x=b*BEAT
    if x>=3.0: add(kick(),x,gain=0.5)
    if x>=6.5: add(hat(),x+BEAT/2,pan=0.2,gain=0.12)
    if x>=9.8 and b%2==1: add(clap(),x,gain=0.13)
    b+=1
# sidechain duck on kicks, master fade
duck=np.ones(N)
for b in range(int(T/BEAT)):
    x=b*BEAT
    if x>=3.0:
        i=int(x*SR); n=min(int(0.25*SR),N-i); duck[i:i+n]=np.minimum(duck[i:i+n],0.55+0.45*np.arange(n)/n)
out*=duck[:,None]
out*=np.minimum(1,t/0.4)[:,None]*np.minimum(1,(T-t)/1.5)[:,None]
out/=np.abs(out).max()/0.8
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out*32767).astype('<i2').tobytes()); w.close(); print('music',T,'s')
