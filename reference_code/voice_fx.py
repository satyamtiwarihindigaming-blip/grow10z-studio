"""Voice moods via pedalboard + a whisper effect. Input: mono float32 array + sample rate. Test: python reference_code/voice_fx.py <wav>"""
import numpy as np
from pedalboard import Pedalboard, Reverb, Compressor, HighpassFilter, LowpassFilter, Gain, Delay, Distortion, Limiter
from scipy.signal import stft, istft
def _run(chain,x,sr): return Pedalboard(chain)(np.asarray(x,dtype=np.float32).reshape(1,-1),sr)[0]
def narration(x,sr): return _run([HighpassFilter(70),Compressor(threshold_db=-20,ratio=2.5),Reverb(room_size=0.25,wet_level=0.12,dry_level=0.9),Gain(2),Limiter(-1)],x,sr)
def tension(x,sr): return _run([HighpassFilter(80),Compressor(threshold_db=-22,ratio=3),Reverb(room_size=0.55,wet_level=0.22,dry_level=0.85),Gain(2),Limiter(-1)],x,sr)
def phone(x,sr): return _run([HighpassFilter(320),LowpassFilter(3400),Distortion(6),Gain(3),Limiter(-1)],x,sr)
def echo(x,sr): return _run([Delay(delay_seconds=0.18,feedback=0.32,mix=0.35),Reverb(room_size=0.5,wet_level=0.2),Limiter(-1)],x,sr)
def whisperize(x,sr):
    f,t,Z=stft(x,sr,nperseg=1024); ph=np.exp(1j*np.random.default_rng(3).uniform(0,2*np.pi,Z.shape))
    _,y=istft(np.abs(Z)*ph,sr,nperseg=1024); return _run([HighpassFilter(300),Gain(4),Limiter(-1)],y[:len(x)],sr)
if __name__=="__main__":
    import soundfile as sf, os, sys
    src=sys.argv[1] if len(sys.argv)>1 else "out/voices/hm_omega.wav"
    x,sr=sf.read(src); x=x[:,0] if x.ndim>1 else x; os.makedirs("out/fx_test",exist_ok=True)
    for n,fn in (("narration",narration),("tension",tension),("phone",phone),("echo",echo),("whisper",whisperize)):
        y=fn(x[:sr*8],sr); y=y/np.max(np.abs(y))*0.9; sf.write(f"out/fx_test/{n}.wav",y.astype(np.float32),sr); print(n,"ok",round(len(y)/sr,1),"s")
