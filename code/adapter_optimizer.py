"""Original low-rank adapter and Adam update. This optional module uses PyTorch."""
import torch
from torch import nn
from torch.nn import functional as F

class SafeSqrt(torch.autograd.Function):
    """Exact sqrt forward, zero v derivative at v=0 (finite Adam composite)."""
    @staticmethod
    def forward(ctx,x):
        out=x.sqrt();ctx.save_for_backward(out);return out
    @staticmethod
    def backward(ctx,g):
        out,=ctx.saved_tensors
        return torch.where(out>0,g/(2*out.clamp_min(1e-30)),torch.zeros_like(g))

def adam(phi,grads,state,lr=5e-4):
    if state is None:state={'t':0,'m':{k:torch.zeros_like(v) for k,v in phi.items()},'v':{k:torch.zeros_like(v) for k,v in phi.items()}}
    t=state['t']+1;m={};v={};p={}
    for k,x in phi.items():
        g=grads[k].float();m[k]=.9*state['m'][k]+.1*g;v[k]=.999*state['v'][k]+.001*g.square()
        p[k]=x-lr*(m[k]/(1-.9**t))/(SafeSqrt.apply(v[k]/(1-.999**t))+1e-8)
    return p,{'t':t,'m':m,'v':v}

def detach_state(phi,state):
    return {k:v.detach().requires_grad_(True) for k,v in phi.items()},None if state is None else {'t':state['t'],'m':{k:v.detach() for k,v in state['m'].items()},'v':{k:v.detach() for k,v in state['v'].items()}}

class AdapterLinear(nn.Module):
    def __init__(self,base,key):
        super().__init__();self.base=base;self.key=key
        self.din=base.in_features;self.dout=base.out_features
        self.fast_a=None;self.fast_b=None;self.capture=False;self.features=[]
    def forward(self,x):
        if self.fast_a is None:return self.base(x)
        # float32 adapters preserve Adam precision; output joins the bf16 path.
        lo=F.linear(F.linear(x.float(),self.fast_a),self.fast_b)*2.
        y=self.base(x)+lo.to(x.dtype)
        if self.capture and y.requires_grad:
            h=x.detach();l=lo.detach()
            y.register_hook(lambda g,h=h,l=l:self.features.append((h,g.detach(),l)))
        return y
