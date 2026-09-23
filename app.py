import argparse, json, math
from statistics import NormalDist
from pathlib import Path

NORMAL = NormalDist()

def sample_size(baseline, mde, alpha=0.05, power=0.8):
    """Approximate required observations per arm for a two-proportion experiment."""
    if not 0 < baseline < 1 or not 0 < mde < 1:
        raise ValueError("baseline and mde must be proportions between 0 and 1")
    target = baseline + mde
    if target >= 1: raise ValueError("baseline + mde must be below 1")
    z_alpha, z_power = NORMAL.inv_cdf(1-alpha/2), NORMAL.inv_cdf(power)
    numerator = (z_alpha * math.sqrt(2*baseline*(1-baseline)) + z_power * math.sqrt(baseline*(1-baseline)+target*(1-target))) ** 2
    return math.ceil(numerator / (target-baseline) ** 2)

def analyze(control_conversions, control_visitors, treatment_conversions, treatment_visitors):
    p1, p2 = control_conversions/control_visitors, treatment_conversions/treatment_visitors
    se = math.sqrt(p1*(1-p1)/control_visitors + p2*(1-p2)/treatment_visitors)
    z = (p2-p1)/se if se else 0
    p_value = 2*(1-NORMAL.cdf(abs(z)))
    return {"control_rate":round(p1,4),"treatment_rate":round(p2,4),
      "absolute_lift":round(p2-p1,4),"relative_lift":round((p2-p1)/p1,4) if p1 else None,
      "incremental_conversions":round((p2-p1)*treatment_visitors,2),
      "p_value":round(p_value,5),"decision":"significant" if p_value < .05 else "inconclusive"}

if __name__ == "__main__":
    parser=argparse.ArgumentParser(description="Plan or analyze an incrementality experiment.")
    parser.add_argument("--baseline",type=float); parser.add_argument("--mde",type=float)
    parser.add_argument("--power",type=float,default=.8); parser.add_argument("--results")
    args=parser.parse_args()
    if args.results:
        data=json.loads(Path(args.results).read_text())
        output=analyze(**data)
    elif args.baseline is not None and args.mde is not None:
        output={"baseline_rate":args.baseline,"minimum_detectable_effect":args.mde,"power":args.power,
                "required_visitors_per_group":sample_size(args.baseline,args.mde,power=args.power)}
    else: parser.error("provide --baseline and --mde, or --results")
    print(json.dumps(output,indent=2))
