"""Bounded static geometry only. No Lezi engine imports, H10 RNG or authority execution."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def board():
 b={}
 for side,y,py,cy in [('black',0,3,2),('red',9,6,7)]:
  for x,t in enumerate(['rook','horse','elephant','advisor','general','advisor','elephant','horse','rook']):b[(x,y)]=(side,t,f'{side}_{t}_{x}')
  for x in (0,2,4,6,8):b[(x,py)]=(side,'pawn',f'{side}_pawn_{x}')
  for x in (1,7):b[(x,cy)]=(side,'cannon',f'{side}_cannon_{x}')
 return b

def between(b,a,z):
 x,y=a;X,Y=z
 if x!=X and y!=Y:return None
 dx=(X>x)-(X<x);dy=(Y>y)-(Y<y);p=(x+dx,y+dy);out=[]
 while p!=z:
  if p in b:out.append(p)
  p=(p[0]+dx,p[1]+dy)
 return out

def attacks(b,a,z,p,stealth=frozenset()):
 side,t,pid=p
 if pid in stealth:return False
 x,y=a;X,Y=z;dx=X-x;dy=Y-y
 if t=='pawn':return (dx==0 and dy==(-1 if side=='red' else 1)) or ((y<=4 if side=='red' else y>=5) and dy==0 and abs(dx)==1)
 if t=='horse':
  if sorted((abs(dx),abs(dy)))!=[1,2]:return False
  leg=(x+dx//2,y) if abs(dx)==2 else (x,y+dy//2)
  return leg not in b
 if t=='elephant':return abs(dx)==abs(dy)==2 and (X>=0 and X<=8) and (Y>=5 if side=='red' else Y<=4) and (x+dx//2,y+dy//2) not in b
 if t=='advisor':return abs(dx)==abs(dy)==1 and 3<=X<=5 and (7<=Y<=9 if side=='red' else 0<=Y<=2)
 if t=='general':return (abs(dx)+abs(dy)==1 and 3<=X<=5 and (7<=Y<=9 if side=='red' else 0<=Y<=2)) or (x==X and b.get(z,('',))[1:2]==('general',) and not between(b,a,z))
 path=between(b,a,z)
 if path is None:return False
 if t=='rook':return len(path) in (0,1) # public M04 concept-threat geometry only, not authority safety algorithm
 if t=='cannon':return len(path)==1
 return False

def public_royal_threats(b,stealth):
 return [{'royal':p[2],'attacker':q[2]} for z,p in b.items() if p[1]=='general' for a,q in b.items() if q[0]!=p[0] and attacks(b,a,z,q,stealth)]

def run():
 d=json.loads((ROOT/'specs/STD_H10_M04_PREFIX_CONTRACT_20261113.json').read_text());b=board();rows=[];stealth=set()
 assert len(b)==32
 assert not public_royal_threats(b,stealth)
 for move in d['prefix']:
  a=tuple(move['from']);z=tuple(move['to']);p=b[a]
  assert p[2]==move['piece'] and z not in b
  if p[1]=='rook':assert between(b,a,z)==[]
  else:assert attacks(b,a,z,p)
  del b[a];b[z]=p
  if move.get('H02_activation'):stealth.add(p[2]) # conditional declared source annotation, not runtime verification
  threats=public_royal_threats(b,stealth);assert not threats,(move,threats)
  assert len(b)==32
  rows.append({'turn':move['turn'],'geometry':'PASS_STATIC','public_royal_threats':threats,'pieces':len(b)})
 a=(0,4);z=(0,2);assert between(b,a,z)==[(0,3)]
 assert b[a][2]=='red_rook_0' and b[z][2]=='black_horse_1'
 assert b[(0,3)][2]=='black_pawn_0'
 assert 'red_rook_0' in stealth
 # Do not execute R5: H10 source qualification and full atomic safety are unverified.
 # Sensitivity controls catch invalid construction, not project behavior.
 wrong=board();assert between(wrong,(0,9),(0,4))==[(0,6)]
 wrong=b.copy();wrong[(0,3)]=('black','pawn','blocker');wrong[(0,5)]=('red','pawn','extra')
 assert len(between(wrong,(0,6),(0,2)))==3 # 0,5 + own rook 0,4 + 0,3
 assert not attacks(b,(0,2),(1,4),b[(0,2)]) # horse leg occupied at0,3
 return {'kind':'SAME_AUTHOR_BOUNDED_STATIC_GEOMETRY','prefix_plies':8,'rows':rows,'target_path':[[0,3]],'target_endpoint':[0,2],'negative_geometry_controls':3,'H02_window':'R4 activation assumed; R5 first subsequent own formal turn','engine_runs':0,'H10_sampling':'UNRUN','R5_authority_execution':'UNRUN','secret_host_true_royal_safety':'NOT_IMPLEMENTED_BY_THIS_CHECKER','full_natural_prefix_proven':False,'independent_QA':False}
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
