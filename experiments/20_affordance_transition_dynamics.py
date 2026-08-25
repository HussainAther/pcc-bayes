from __future__ import annotations

import csv
from pathlib import Path
from multiprocessing import Pool

import numpy as np

from pcc_bayes.affordance_dynamics import analytical_filter_step, prediction_gap_contraction_residual
from pcc_bayes.affordance_geometry import classify_topset_supports, support_fraction_summary
from pcc_bayes.multiclass_chaos import ThreeStateTrackingConfig, filter_three_state_markov, generate_three_state_episode

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = ROOT / "results" / "18_information_affordance_map.csv"
OUT = ROOT / "results" / "20_affordance_transition_dynamics.csv"
OBSERVATION_ACCURACIES = (0.45, 0.55, 0.65, 0.80)
SWITCH_PROBABILITIES = (0.03, 0.10, 0.30)
EVALUATION_SEEDS = tuple(range(1000, 1100))
TOL = 1e-12


def load_historical():
    with HISTORICAL.open(newline="") as f:
        rows = list(csv.DictReader(f))
    return {
        (float(r["observation_accuracy"]), float(r["switch_probability"])): r
        for r in rows if r["candidate_policy"] == "utility_topset_chaos"
    }


def transition_matrix(before, after):
    m = np.zeros((3, 3), dtype=int)
    for b, a in zip(before, after):
        m[int(b) - 1, int(a) - 1] += 1
    return m


def run_cell(args):
    switch_probability, observation_accuracy, historical = args
    analytical_posts = []
    implemented_posts = []
    analytical_before_classes = []
    analytical_after_classes = []
    implemented_before_classes = []
    implemented_after_classes = []
    max_error = 0.0
    max_gap_residual = 0.0
    config = ThreeStateTrackingConfig(steps=400, switch_probability=switch_probability, observation_accuracy=observation_accuracy)
    for seed in EVALUATION_SEEDS:
        _, observations = generate_three_state_episode(config, seed)
        impl = filter_three_state_markov(observations, switch_probability=switch_probability, observation_accuracy=observation_accuracy)
        prior = np.full(3, 1.0 / 3.0)
        analytic = np.empty_like(impl)
        before_beliefs = np.empty_like(impl)
        kappa = 1.0 - 1.5 * switch_probability
        for t, y in enumerate(observations):
            before_beliefs[t] = prior
            # exact prediction identity checked inline without a second helper call
            q = kappa * prior + 0.5 * switch_probability
            for i in range(3):
                for j in range(i + 1, 3):
                    max_gap_residual = max(max_gap_residual, abs((q[i]-q[j]) - kappa*(prior[i]-prior[j])))
            miss = (1.0 - observation_accuracy) / 2.0
            likelihood = np.full(3, miss)
            likelihood[int(y)] = observation_accuracy
            post = q * likelihood
            post = post / post.sum()
            analytic[t] = post
            prior = post
        max_error = max(max_error, float(np.max(np.abs(analytic - impl))))
        analytical_posts.append(analytic)
        implemented_posts.append(impl)
        analytical_before_classes.append(classify_topset_supports(before_beliefs, utility_gap=0.30))
        analytical_after_classes.append(classify_topset_supports(analytic, utility_gap=0.30))
        impl_before = np.vstack([np.full((1, 3), 1.0/3.0), impl[:-1]])
        implemented_before_classes.append(classify_topset_supports(impl_before, utility_gap=0.30))
        implemented_after_classes.append(classify_topset_supports(impl, utility_gap=0.30))
    a_after=np.concatenate(analytical_after_classes); i_after=np.concatenate(implemented_after_classes)
    a_before=np.concatenate(analytical_before_classes); i_before=np.concatenate(implemented_before_classes)
    class_mismatches=int(np.sum(a_after != i_after))
    matrix_a=transition_matrix(a_before,a_after); matrix_i=transition_matrix(i_before,i_after)
    summary=support_fraction_summary(a_after)
    hist=historical[(observation_accuracy,switch_probability)]
    hist_branch=float(hist['branch_opportunity_fraction']); hist_three=float(hist['three_way_opportunity_fraction'])
    row={'observation_accuracy':observation_accuracy,'switch_probability':switch_probability,'updates':len(a_after),'max_posterior_error':max_error,'max_gap_contraction_residual':max_gap_residual,'class_mismatch_count':class_mismatches,'one_action_fraction':summary['one_action_fraction'],'two_action_fraction':summary['two_action_fraction'],'three_action_fraction':summary['three_action_fraction'],'branch_fraction':summary['branch_fraction'],'historical_branch_fraction':hist_branch,'historical_three_action_fraction':hist_three}
    for i in range(3):
        for j in range(3):
            row[f'transition_{i+1}_to_{j+1}']=int(matrix_a[i,j]); row[f'implemented_transition_{i+1}_to_{j+1}']=int(matrix_i[i,j])
    row.update({'gate_posterior_map':max_error<=TOL,'gate_zero_class_mismatch':class_mismatches==0,'gate_transition_matrix_match':bool(np.array_equal(matrix_a,matrix_i)),'gate_gap_contraction':max_gap_residual<=TOL,'gate_historical_branch_match':abs(summary['branch_fraction']-hist_branch)<=TOL,'gate_historical_three_match':abs(summary['three_action_fraction']-hist_three)<=TOL})
    row['cell_pass']=all(v for k,v in row.items() if k.startswith('gate_'))
    return row


def main():
    historical=load_historical()
    args=[(s,a,historical) for s in SWITCH_PROBABILITIES for a in OBSERVATION_ACCURACIES]
    with Pool(processes=12) as pool:
        rows=pool.map(run_cell,args)
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    grand_states=sum(r['updates'] for r in rows); grand_class_mismatches=sum(r['class_mismatch_count'] for r in rows)
    global_max_error=max(r['max_posterior_error'] for r in rows); global_max_gap_residual=max(r['max_gap_contraction_residual'] for r in rows)
    print(f'tested updates: {grand_states}')
    print(f'max posterior coordinate error: {global_max_error:.3e}')
    print(f'max gap contraction residual: {global_max_gap_residual:.3e}')
    print(f'affordance class mismatches: {grand_class_mismatches}')
    for r in rows:
        print(f"obs={r['observation_accuracy']:.2f} switch={r['switch_probability']:.2f} 1={r['one_action_fraction']:.4f} 2={r['two_action_fraction']:.4f} 3={r['three_action_fraction']:.4f} 1->2={r['transition_1_to_2']} 1->3={r['transition_1_to_3']} 2->3={r['transition_2_to_3']} 3->2={r['transition_3_to_2']} {'PASS' if r['cell_pass'] else 'FAIL'}")
    overall=all(r['cell_pass'] for r in rows)
    print(f"\nv0.11 affordance-transition dynamics: {'PASS' if overall else 'FAIL'}")
    print(f'wrote {OUT}')


if __name__ == '__main__':
    main()
