"""Read-only live DOM structure probe; does not compute layout or alter the game."""
PROBE = r"""() => {
  const body=document.body;
  if(!body) throw Error('missing body');
  let elements=0,maxDepth=0,maxChildren=body.childElementCount;
  const stack=Array.from(body.children,e=>[e,2]);
  const ids=new Map();
  while(stack.length){
    const [e,d]=stack.pop();
    elements++;maxDepth=Math.max(maxDepth,d);
    maxChildren=Math.max(maxChildren,e.childElementCount);
    if(e.id)ids.set(e.id,(ids.get(e.id)||0)+1);
    for(const c of e.children)stack.push([c,d+1]);
  }
  if(body.id)ids.set(body.id,(ids.get(body.id)||0)+1);
  return {elements,maxDepth,maxChildren,
    duplicateIds:[...ids].filter(([id,n])=>n>1).map(([id,n])=>({id,count:n})),
    styleBlocks:document.querySelectorAll('style').length,
    stylesheetLinks:document.querySelectorAll('link[rel~="stylesheet"]').length};
}"""

def measure_dom(page, label):
    result=page.evaluate(PROBE)
    issues=[]
    if result["elements"]>1400:issues.append("D05 elements >1400")
    elif result["elements"]>800:issues.append("D05 elements >800")
    if result["maxDepth"]>32:issues.append("D05 depth >32")
    if result["maxChildren"]>60:issues.append("D05 children >60")
    if result["duplicateIds"]:issues.append("D09 duplicate IDs")
    if result["styleBlocks"]!=1 or result["stylesheetLinks"]:issues.append("C01 style owner")
    return {"label":label,**result,"findings":issues,"status":"REVIEW_REQUIRED" if issues else "WITHIN_MEASURED_LIMITS"}
