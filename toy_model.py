#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
toy_model.py
Modelo mínimo de "Ventana de Resiliencia" (v1.0)

Requisitos:
  pip install numpy matplotlib

Uso rápido:
  python toy_model.py --sweep

Ejemplo (un tau):
  python toy_model.py --tau 12 --steps 20000 --plot
"""

from __future__ import annotations

import argparse
import math
import os
from dataclasses import dataclass, asdict
from typing import Dict, Tuple, List

import numpy as np


@dataclass
class Params:
    # entorno
    omega: float = 2 * math.pi / 800.0   # señal lenta
    sigma_e: float = 0.20                # ruido entorno

    # dinámica
    gamma: float = 0.02                  # amortiguación
    eta: float = 0.35                    # término correctivo (error)
    sigma: float = 0.06                  # término generativo (error^3)

    # simulación
    steps: int = 20000
    burn_in: int = 2000
    seed: int = 7


def simulate(tau: float, p: Params) -> Dict[str, np.ndarray]:
    """
    Simula el toy model para un tau dado.

    Modelo:
      e_t = sin(omega t) + N(0, sigma_e^2)
      M_t = (1 - alpha) M_{t-1} + alpha x_t, con alpha = 1/tau
      ehat_t = M_t
      eps_t = e_t - ehat_t
      x_{t+1} = (1-gamma) x_t + tanh(M_t) + eta*eps_t + sigma*(eps_t^3)
    """
    if tau <= 0:
        raise ValueError("tau debe ser > 0")

    rng = np.random.default_rng(p.seed)
    alpha = 1.0 / tau

    x = np.zeros(p.steps + 1, dtype=np.float64)
    M = np.zeros(p.steps + 1, dtype=np.float64)
    e = np.zeros(p.steps + 1, dtype=np.float64)
    ehat = np.zeros(p.steps + 1, dtype=np.float64)
    eps = np.zeros(p.steps + 1, dtype=np.float64)

    for t in range(p.steps):
        # entorno
        e[t] = math.sin(p.omega * t) + rng.normal(0.0, p.sigma_e)

        # predicción y error
        ehat[t] = M[t]
        eps[t] = e[t] - ehat[t]

        # dinámica del estado
        x[t + 1] = (
            (1.0 - p.gamma) * x[t]
            + math.tanh(M[t])
            + p.eta * eps[t]
            + p.sigma * (eps[t] ** 3)
        )

        # memoria (promedio exponencial)
        M[t + 1] = (1.0 - alpha) * M[t] + alpha * x[t + 1]

    # último punto de entorno (solo para tener arrays alineados)
    e[p.steps] = math.sin(p.omega * p.steps) + rng.normal(0.0, p.sigma_e)
    ehat[p.steps] = M[p.steps]
    eps[p.steps] = e[p.steps] - ehat[p.steps]

    return {"x": x, "M": M, "e": e, "ehat": ehat, "eps": eps}


def metrics(sim: Dict[str, np.ndarray], p: Params) -> Dict[str, float]:
    """
    Métricas simples para ver regímenes:
      - track_rmse: qué tan bien sigue al entorno (error de predicción)
      - volatility: cuán errático es x (std de dx)
      - rigidity: qué tan "congelado" está (1 / (std|dx| + eps))
      - resilience_score: heurística que favorece bajo rmse y volatilidad moderada
    """
    x = sim["x"][p.burn_in:]
    e = sim["e"][p.burn_in:]
    ehat = sim["ehat"][p.burn_in:]

    eps = e - ehat
    track_rmse = float(np.sqrt(np.mean(eps ** 2)))

    dx = np.diff(x)
    volatility = float(np.std(dx))

    # rigidez: grande si el sistema casi no cambia
    rigidity = float(1.0 / (np.mean(np.abs(dx)) + 1e-9))

    # score simple: penaliza rmse y extremos de volatilidad (demasiado baja = rigidez, demasiado alta = caos)
    # target_vol: una escala "moderada" relativa al propio dx.
    target_vol = 0.5 * (np.percentile(np.abs(dx), 90) + 1e-9)
    vol_penalty = abs(volatility - target_vol) / (target_vol + 1e-9)

    resilience_score = float(1.0 / (track_rmse + 1e-9) * 1.0 / (1.0 + vol_penalty))

    return {
        "track_rmse": track_rmse,
        "volatility": volatility,
        "rigidity": rigidity,
        "resilience_score": resilience_score,
    }


def sweep_taus(
    taus: np.ndarray,
    p: Params,
) -> Tuple[np.ndarray, List[Dict[str, float]]]:
    rows: List[Dict[str, float]] = []
    for tau in taus:
        sim = simulate(float(tau), p)
        m = metrics(sim, p)
        m["tau"] = float(tau)
        rows.append(m)
    return taus, rows


def save_csv(path: str, rows: List[Dict[str, float]]) -> None:
    import csv
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    keys = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def plot_single(sim: Dict[str, np.ndarray], p: Params, outpath: str) -> None:
    import matplotlib.pyplot as plt

    t = np.arange(len(sim["x"]))
    start = p.burn_in
    end = min(len(t), start + 2500)  # ventana para visualizar

    plt.figure()
    plt.plot(t[start:end], sim["e"][start:end], label="e_t (entorno)")
    plt.plot(t[start:end], sim["ehat"][start:end], label="ê_t = M_t (predicción)")
    plt.plot(t[start:end], sim["x"][start:end], label="x_t (estado)")
    plt.xlabel("t")
    plt.title("Toy model (tramo post burn-in)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


def plot_sweep(rows: List[Dict[str, float]], outpath: str) -> None:
    import matplotlib.pyplot as plt

    tau = np.array([r["tau"] for r in rows], dtype=float)
    rmse = np.array([r["track_rmse"] for r in rows], dtype=float)
    vol = np.array([r["volatility"] for r in rows], dtype=float)
    rig = np.array([r["rigidity"] for r in rows], dtype=float)
    score = np.array([r["resilience_score"] for r in rows], dtype=float)

    plt.figure()
    plt.plot(tau, score, label="resilience_score")
    plt.xscale("log")
    plt.xlabel("tau (log)")
    plt.title("Ventana de resiliencia (heurística)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath.replace(".png", "_score.png"), dpi=200)
    plt.close()

    plt.figure()
    plt.plot(tau, rmse, label="track_rmse")
    plt.xscale("log")
    plt.xlabel("tau (log)")
    plt.title("Seguimiento del entorno (RMSE)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath.replace(".png", "_rmse.png"), dpi=200)
    plt.close()

    plt.figure()
    plt.plot(tau, vol, label="volatility (std dx)")
    plt.plot(tau, rig, label="rigidity (1/mean|dx|)")
    plt.xscale("log")
    plt.xlabel("tau (log)")
    plt.title("Caos vs Rigidez (proxies)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath.replace(".png", "_chaos_rigidity.png"), dpi=200)
    plt.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tau", type=float, default=12.0, help="Escala de memoria tau (>0)")
    ap.add_argument("--steps", type=int, default=20000, help="Pasos totales")
    ap.add_argument("--burn-in", dest="burn_in", type=int, default=2000, help="Pasos iniciales descartados")
    ap.add_argument("--seed", type=int, default=7, help="Semilla RNG")
    ap.add_argument("--omega", type=float, default=2 * math.pi / 800.0, help="Frecuencia entorno (lenta)")
    ap.add_argument("--sigma-e", dest="sigma_e", type=float, default=0.20, help="Std del ruido del entorno")
    ap.add_argument("--gamma", type=float, default=0.02, help="Amortiguación")
    ap.add_argument("--eta", type=float, default=0.35, help="Ganancia correctiva (error)")
    ap.add_argument("--sigma", type=float, default=0.06, help="Ganancia generativa (error^3)")

    ap.add_argument("--plot", action="store_true", help="Guardar plot de una corrida")
    ap.add_argument("--sweep", action="store_true", help="Barrer taus para ver ventana")
    ap.add_argument("--tau-min", dest="tau_min", type=float, default=0.5, help="Tau mínimo (sweep)")
    ap.add_argument("--tau-max", dest="tau_max", type=float, default=200.0, help="Tau máximo (sweep)")
    ap.add_argument("--tau-n", dest="tau_n", type=int, default=40, help="Cantidad de taus (sweep)")
    ap.add_argument("--outdir", type=str, default="out", help="Directorio de salida")

    args = ap.parse_args()

    p = Params(
        omega=args.omega,
        sigma_e=args.sigma_e,
        gamma=args.gamma,
        eta=args.eta,
        sigma=args.sigma,
        steps=args.steps,
        burn_in=args.burn_in,
        seed=args.seed,
    )

    os.makedirs(args.outdir, exist_ok=True)

    if args.sweep:
        taus = np.logspace(math.log10(args.tau_min), math.log10(args.tau_max), args.tau_n)
        _, rows = sweep_taus(taus, p)
        csv_path = os.path.join(args.outdir, "sweep_metrics.csv")
        save_csv(csv_path, rows)
        plot_sweep(rows, os.path.join(args.outdir, "sweep.png"))
        print(f"[OK] Sweep guardado: {csv_path}")
        print(f"[OK] Plots guardados en: {args.outdir}/sweep_*png")
        # imprime el mejor tau según score
        best = max(rows, key=lambda r: r["resilience_score"])
        print("[BEST] tau =", best["tau"], "score =", best["resilience_score"])
        return

    sim = simulate(args.tau, p)
    m = metrics(sim, p)
    print("[PARAMS]", asdict(p))
    print("[TAU]", args.tau)
    print("[METRICS]", m)

    if args.plot:
        outpath = os.path.join(args.outdir, f"run_tau_{args.tau:.3g}.png")
        plot_single(sim, p, outpath)
        print(f"[OK] Plot guardado: {outpath}")


if __name__ == "__main__":
    main()
