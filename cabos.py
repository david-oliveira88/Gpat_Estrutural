from __future__ import annotations
"""Módulo: cabos.py

Banco de dados de cabos condutores e para-raios com função factory
para criação automática de instâncias da classe Cabo.

Este código foi atualizado com base no "Catálogo Técnico Condutores
Elétricos de Alumínio" da Alubar (2015). Os dados foram extraídos
das tabelas correspondentes e as unidades foram convertidas quando
necessário (ex: kN para kgf).

Uso:
    from cabos import criar_cabo, listar_cabos

    cabo = criar_cabo("Linnet")
    print(cabo.peso_unit_npm)  # Exemplo de uso, depende da classe Cabo

    cabos_disponiveis = listar_cabos()
"""
from typing import Dict, List, Optional
# A classe Cabo é esperada em um módulo chamado 'elementos'
# from elementos import Cabo

# Fator de conversão de kN para kgf
KN_PARA_KGF = 101.971621
# Fator de conversão de MPa para kgf/mm2
MPA_PARA_KGFMM2 = 0.101971621

# ====================================================================
# Base de dados de cabos condutores CAA (Alumínio com Alma de Aço)
# Fonte: Catálogo Alubar 2015, Páginas 21-26
# ====================================================================
CABOS_CAA = {
    # Cabos com formação 6 Fios Al / 1 Fio Aço
    # Módulo Elasticidade: 79 GPa, Coef. Dilatação: 19.1e-6 /°C
    "Turkey": {
        "diametro_mm": 5.04, "area_secao_total_mm2": 15.52, "area_secao_al_mm2": 13.30, "area_secao_aco_mm2": 2.22,
        "peso_total_kgfm": 0.05374, "peso_al_kgfm": 0.03664, "peso_aco_kgfm": 0.01710,
        "modulo_elasticidade_kgfmm2": 79 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.91e-5,
        "carga_ruptura_kgf": 5.30 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 2.1498
    },
    "Thrush": {
        "diametro_mm": 5.67, "area_secao_total_mm2": 19.64, "area_secao_al_mm2": 16.83, "area_secao_aco_mm2": 2.81,
        "peso_total_kgfm": 0.06801, "peso_al_kgfm": 0.04637, "peso_aco_kgfm": 0.02164,
        "modulo_elasticidade_kgfmm2": 79 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.91e-5,
        "carga_ruptura_kgf": 6.65 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 1.6986
    },
    "Swan": {
        "diametro_mm": 6.36, "area_secao_total_mm2": 24.71, "area_secao_al_mm2": 21.18, "area_secao_aco_mm2": 3.53,
        "peso_total_kgfm": 0.08557, "peso_al_kgfm": 0.05834, "peso_aco_kgfm": 0.02723,
        "modulo_elasticidade_kgfmm2": 79 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.91e-5,
        "carga_ruptura_kgf": 8.30 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 1.3500
    },
    "Swallow": {
        "diametro_mm": 7.14, "area_secao_total_mm2": 31.14, "area_secao_al_mm2": 26.69, "area_secao_aco_mm2": 4.45,
        "peso_total_kgfm": 0.10784, "peso_al_kgfm": 0.07353, "peso_aco_kgfm": 0.03432,
        "modulo_elasticidade_kgfmm2": 79 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.91e-5,
        "carga_ruptura_kgf": 10.23 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 1.0712
    },
    "Sparrow": {
        "diametro_mm": 8.01, "area_secao_total_mm2": 39.19, "area_secao_al_mm2": 33.59, "area_secao_aco_mm2": 5.60,
        "peso_total_kgfm": 0.13573, "peso_al_kgfm": 0.09253, "peso_aco_kgfm": 0.04319,
        "modulo_elasticidade_kgfmm2": 79 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.91e-5,
        "carga_ruptura_kgf": 12.65 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.8511
    },
    "Robin": {
        "diametro_mm": 9.00, "area_secao_total_mm2": 49.48, "area_secao_al_mm2": 42.41, "area_secao_aco_mm2": 7.07,
        "peso_total_kgfm": 0.17135, "peso_al_kgfm": 0.11682, "peso_aco_kgfm": 0.05453,
        "modulo_elasticidade_kgfmm2": 79 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.91e-5,
        "carga_ruptura_kgf": 15.85 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.6742
    },
    "Raven": {
        "diametro_mm": 10.11, "area_secao_total_mm2": 62.44, "area_secao_al_mm2": 53.52, "area_secao_aco_mm2": 8.92,
        "peso_total_kgfm": 0.21622, "peso_al_kgfm": 0.14742, "peso_aco_kgfm": 0.06881,
        "modulo_elasticidade_kgfmm2": 79 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.91e-5,
        "carga_ruptura_kgf": 19.45 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.5343
    },
    "Quail": {
        "diametro_mm": 11.34, "area_secao_total_mm2": 78.55, "area_secao_al_mm2": 67.33, "area_secao_aco_mm2": 11.22,
        "peso_total_kgfm": 0.27204, "peso_al_kgfm": 0.18547, "peso_aco_kgfm": 0.08657,
        "modulo_elasticidade_kgfmm2": 79 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.91e-5,
        "carga_ruptura_kgf": 23.53 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.4246
    },
    "Pigeon": {
        "diametro_mm": 12.75, "area_secao_total_mm2": 99.30, "area_secao_al_mm2": 85.12, "area_secao_aco_mm2": 14.19,
        "peso_total_kgfm": 0.34389, "peso_al_kgfm": 0.23446, "peso_aco_kgfm": 0.10944,
        "modulo_elasticidade_kgfmm2": 79 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.91e-5,
        "carga_ruptura_kgf": 29.42 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.3359
    },
    "Penguin": {
        "diametro_mm": 14.31, "area_secao_total_mm2": 125.09, "area_secao_al_mm2": 107.22, "area_secao_aco_mm2": 17.87,
        "peso_total_kgfm": 0.43319, "peso_al_kgfm": 0.29534, "peso_aco_kgfm": 0.13786,
        "modulo_elasticidade_kgfmm2": 79 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.91e-5,
        "carga_ruptura_kgf": 37.06 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.2667
    },
    # Cabos com formação 18 Fios Al / 1 Fio Aço
    # Módulo Elasticidade: 68 GPa, Coef. Dilatação: 21.2e-6 /°C
    "Waxwing": {
        "diametro_mm": 15.45, "area_secao_total_mm2": 142.48, "area_secao_al_mm2": 134.98, "area_secao_aco_mm2": 7.50,
        "peso_total_kgfm": 0.43050, "peso_al_kgfm": 0.37271, "peso_aco_kgfm": 0.05778,
        "modulo_elasticidade_kgfmm2": 68 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.12e-5,
        "carga_ruptura_kgf": 31.22 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.2129
    },
    "Merlin": {
        "diametro_mm": 17.35, "area_secao_total_mm2": 179.68, "area_secao_al_mm2": 170.22, "area_secao_aco_mm2": 9.46,
        "peso_total_kgfm": 0.54289, "peso_al_kgfm": 0.47002, "peso_aco_kgfm": 0.07287,
        "modulo_elasticidade_kgfmm2": 68 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.12e-5,
        "carga_ruptura_kgf": 39.36 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1688
    },
    "Chickadee": {
        "diametro_mm": 18.85, "area_secao_total_mm2": 212.09, "area_secao_al_mm2": 200.93, "area_secao_aco_mm2": 11.16,
        "peso_total_kgfm": 0.64082, "peso_al_kgfm": 0.55481, "peso_aco_kgfm": 0.08602,
        "modulo_elasticidade_kgfmm2": 68 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.12e-5,
        "carga_ruptura_kgf": 45.14 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1430
    },
    "Pelican": {
        "diametro_mm": 20.70, "area_secao_total_mm2": 255.77, "area_secao_al_mm2": 242.31, "area_secao_aco_mm2": 13.46,
        "peso_total_kgfm": 0.77278, "peso_al_kgfm": 0.66905, "peso_aco_kgfm": 0.10373,
        "modulo_elasticidade_kgfmm2": 68 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.12e-5,
        "carga_ruptura_kgf": 53.50 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1186
    },
    "Osprey": {
        "diametro_mm": 22.35, "area_secao_total_mm2": 298.17, "area_secao_al_mm2": 282.47, "area_secao_aco_mm2": 15.69,
        "peso_total_kgfm": 0.90089, "peso_al_kgfm": 0.77996, "peso_aco_kgfm": 0.12092,
        "modulo_elasticidade_kgfmm2": 68 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.12e-5,
        "carga_ruptura_kgf": 61.32 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1017
    },
    "Kingbird": {
        "diametro_mm": 23.90, "area_secao_total_mm2": 340.96, "area_secao_al_mm2": 323.01, "area_secao_aco_mm2": 17.95,
        "peso_total_kgfm": 1.03018, "peso_al_kgfm": 0.89190, "peso_aco_kgfm": 0.13828,
        "modulo_elasticidade_kgfmm2": 68 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.12e-5,
        "carga_ruptura_kgf": 70.12 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0890
    },
    # Cabos com formação 24, 26, 54 Fios Al / 7 Fios Aço
    # Módulo Elasticidade: 74 GPa (26/7), 67 GPa (54/7), Coef. Dilatação: 18.9e-6 (26/7), 19.4e-6 (54/7) /°C
    "Partridge": {
        "diametro_mm": 16.28, "area_secao_total_mm2": 156.87, "area_secao_al_mm2": 134.87, "area_secao_aco_mm2": 21.99,
        "peso_total_kgfm": 0.54546, "peso_al_kgfm": 0.37400, "peso_aco_kgfm": 0.17146,
        "modulo_elasticidade_kgfmm2": 74 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-5,
        "carga_ruptura_kgf": 50.11 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.2141
    },
    "Ostrich": {
        "diametro_mm": 17.28, "area_secao_total_mm2": 176.90, "area_secao_al_mm2": 152.19, "area_secao_aco_mm2": 24.71,
        "peso_total_kgfm": 0.61466, "peso_al_kgfm": 0.42201, "peso_aco_kgfm": 0.19265,
        "modulo_elasticidade_kgfmm2": 74 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-5,
        "carga_ruptura_kgf": 54.75 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1897
    },
    "Linnet": {
        "diametro_mm": 18.31, "area_secao_total_mm2": 198.39, "area_secao_al_mm2": 170.55, "area_secao_aco_mm2": 27.83,
        "peso_total_kgfm": 0.68993, "peso_al_kgfm": 0.47293, "peso_aco_kgfm": 0.21700,
        "modulo_elasticidade_kgfmm2": 74 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-5,
        "carga_ruptura_kgf": 62.92 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1693
    },
    "Ibis": {
        "diametro_mm": 19.88, "area_secao_total_mm2": 234.07, "area_secao_al_mm2": 201.34, "area_secao_aco_mm2": 32.73,
        "peso_total_kgfm": 0.81349, "peso_al_kgfm": 0.55829, "peso_aco_kgfm": 0.25520,
        "modulo_elasticidade_kgfmm2": 74 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-5,
        "carga_ruptura_kgf": 70.23 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1434
    },
    "Hawk": {
        "diametro_mm": 21.80, "area_secao_total_mm2": 281.13, "area_secao_al_mm2": 241.65, "area_secao_aco_mm2": 39.49,
        "peso_total_kgfm": 0.97794, "peso_al_kgfm": 0.67007, "peso_aco_kgfm": 0.30787,
        "modulo_elasticidade_kgfmm2": 74 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-5,
        "carga_ruptura_kgf": 84.52 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1195
    },
    "Dove": {
        "diametro_mm": 23.55, "area_secao_total_mm2": 328.50, "area_secao_al_mm2": 282.59, "area_secao_aco_mm2": 45.92,
        "peso_total_kgfm": 1.14159, "peso_al_kgfm": 0.78358, "peso_aco_kgfm": 0.35801,
        "modulo_elasticidade_kgfmm2": 74 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-5,
        "carga_ruptura_kgf": 97.75 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1022
    },
    "Grosbeak": {
        "diametro_mm": 25.15, "area_secao_total_mm2": 374.34, "area_secao_al_mm2": 321.84, "area_secao_aco_mm2": 52.49,
        "peso_total_kgfm": 1.30172, "peso_al_kgfm": 0.89244, "peso_aco_kgfm": 0.40928,
        "modulo_elasticidade_kgfmm2": 74 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-5,
        "carga_ruptura_kgf": 108.35 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0897
    },
    "Starling": {
        "diametro_mm": 26.68, "area_secao_total_mm2": 421.08, "area_secao_al_mm2": 361.93, "area_secao_aco_mm2": 59.15,
        "peso_total_kgfm": 1.46477, "peso_al_kgfm": 1.00361, "peso_aco_kgfm": 0.46116,
        "modulo_elasticidade_kgfmm2": 74 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-5,
        "carga_ruptura_kgf": 121.97 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0798
    },
    "Drake": {
        "diametro_mm": 28.11, "area_secao_total_mm2": 468.00, "area_secao_al_mm2": 402.56, "area_secao_aco_mm2": 65.44,
        "peso_total_kgfm": 1.62646, "peso_al_kgfm": 1.11626, "peso_aco_kgfm": 0.51020,
        "modulo_elasticidade_kgfmm2": 74 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-5,
        "carga_ruptura_kgf": 135.27 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0717
    },
    "Gannet": {
        "diametro_mm": 25.76, "area_secao_total_mm2": 393.16, "area_secao_al_mm2": 338.26, "area_secao_aco_mm2": 54.90,
        "peso_total_kgfm": 1.36600, "peso_al_kgfm": 0.93797, "peso_aco_kgfm": 0.42803,
        "modulo_elasticidade_kgfmm2": 74 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-5,
        "carga_ruptura_kgf": 113.57 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0854
    },
    "Condor": {
        "diametro_mm": 27.72, "area_secao_total_mm2": 454.49, "area_secao_al_mm2": 402.33, "area_secao_aco_mm2": 52.15,
        "peso_total_kgfm": 1.52208, "peso_al_kgfm": 1.11486, "peso_aco_kgfm": 0.40722,
        "modulo_elasticidade_kgfmm2": 67 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.94e-5,
        "carga_ruptura_kgf": 121.55 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0718
    },
    "Cardinal": {
        "diametro_mm": 30.42, "area_secao_total_mm2": 547.33, "area_secao_al_mm2": 484.53, "area_secao_aco_mm2": 62.81,
        "peso_total_kgfm": 1.83302, "peso_al_kgfm": 1.34262, "peso_aco_kgfm": 0.49041,
        "modulo_elasticidade_kgfmm2": 67 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.94e-5,
        "carga_ruptura_kgf": 146.38 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0596
    },
    "Curlew": {
        "diametro_mm": 31.59, "area_secao_total_mm2": 590.25, "area_secao_al_mm2": 522.51, "area_secao_aco_mm2": 67.73,
        "peso_total_kgfm": 1.97674, "peso_al_kgfm": 1.44788, "peso_aco_kgfm": 0.52886,
        "modulo_elasticidade_kgfmm2": 67 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.94e-5,
        "carga_ruptura_kgf": 157.86 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0553
    },
    # Cabos com formação 30 Fios Al / 7 ou 19 Fios Aço
    # Módulo Elasticidade: 78 GPa (30/7), 75 GPa (30/19), Coef. Dilatação: 17.8e-6 (30/7), 18.0e-6 (30/19) /°C
    "Oriole": {
        "diametro_mm": 18.83, "area_secao_total_mm2": 210.28, "area_secao_al_mm2": 170.50, "area_secao_aco_mm2": 39.78,
        "peso_total_kgfm": 0.78427, "peso_al_kgfm": 0.47359, "peso_aco_kgfm": 0.31068,
        "modulo_elasticidade_kgfmm2": 78 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.78e-5,
        "carga_ruptura_kgf": 74.59 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1698
    },
    "Lark": {
        "diametro_mm": 20.44, "area_secao_total_mm2": 247.77, "area_secao_al_mm2": 200.90, "area_secao_aco_mm2": 46.88,
        "peso_total_kgfm": 0.92412, "peso_al_kgfm": 0.55804, "peso_aco_kgfm": 0.36608,
        "modulo_elasticidade_kgfmm2": 78 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.78e-5,
        "carga_ruptura_kgf": 87.33 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1441
    },
    "Hen": {
        "diametro_mm": 22.40, "area_secao_total_mm2": 297.57, "area_secao_al_mm2": 241.27, "area_secao_aco_mm2": 56.30,
        "peso_total_kgfm": 1.10984, "peso_al_kgfm": 0.67020, "peso_aco_kgfm": 0.43965,
        "modulo_elasticidade_kgfmm2": 78 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.78e-5,
        "carga_ruptura_kgf": 101.83 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1200
    },
    "Eagle": {
        "diametro_mm": 24.22, "area_secao_total_mm2": 347.89, "area_secao_al_mm2": 282.07, "area_secao_aco_mm2": 65.80,
        "peso_total_kgfm": 1.29752, "peso_al_kgfm": 0.78353, "peso_aco_kgfm": 0.51399,
        "modulo_elasticidade_kgfmm2": 78 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.78e-5,
        "carga_ruptura_kgf": 119.05 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1026
    },
    "Wood_Duck": {
        "diametro_mm": 25.27, "area_secao_total_mm2": 378.71, "area_secao_al_mm2": 307.06, "area_secao_aco_mm2": 71.65,
        "peso_total_kgfm": 1.41246, "peso_al_kgfm": 0.85294, "peso_aco_kgfm": 0.55953,
        "modulo_elasticidade_kgfmm2": 78 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.78e-5,
        "carga_ruptura_kgf": 123.92 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0943
    },
    "Scoter": {
        "diametro_mm": 25.90, "area_secao_total_mm2": 397.83, "area_secao_al_mm2": 322.56, "area_secao_aco_mm2": 75.26,
        "peso_total_kgfm": 1.48377, "peso_al_kgfm": 0.89599, "peso_aco_kgfm": 0.58777,
        "modulo_elasticidade_kgfmm2": 78 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.78e-5,
        "carga_ruptura_kgf": 130.18 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0897
    },
    "Redwing": {
        "diametro_mm": 27.43, "area_secao_total_mm2": 444.47, "area_secao_al_mm2": 362.06, "area_secao_aco_mm2": 82.41,
        "peso_total_kgfm": 1.65056, "peso_al_kgfm": 1.00543, "peso_aco_kgfm": 0.64513,
        "modulo_elasticidade_kgfmm2": 75 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.80e-5,
        "carga_ruptura_kgf": 148.29 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0799
    },
    "Mallard": {
        "diametro_mm": 28.96, "area_secao_total_mm2": 495.62, "area_secao_al_mm2": 403.84, "area_secao_aco_mm2": 91.78,
        "peso_total_kgfm": 1.83994, "peso_al_kgfm": 1.12146, "peso_aco_kgfm": 0.71848,
        "modulo_elasticidade_kgfmm2": 75 * 1000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.80e-5,
        "carga_ruptura_kgf": 165.25 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0717
    },
    # E muitos outros cabos CAA... A lista completa está abaixo.
    # Adicionando os demais cabos CAA do catálogo
    "Brant": {"diametro_mm": 19.62, "area_secao_total_mm2": 227.68, "area_secao_al_mm2": 201.56, "area_secao_aco_mm2": 26.13, "peso_total_kgfm": 0.76251, "peso_al_kgfm": 0.55886, "peso_aco_kgfm": 0.20365, "modulo_elasticidade_kgfmm2": 74000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-05, "carga_ruptura_kgf": 63.34 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1433},
    "Flicker": {"diametro_mm": 21.49, "area_secao_total_mm2": 272.99, "area_secao_al_mm2": 241.58, "area_secao_aco_mm2": 31.4, "peso_total_kgfm": 0.91462, "peso_al_kgfm": 0.66985, "peso_aco_kgfm": 0.24477, "modulo_elasticidade_kgfmm2": 74000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-05, "carga_ruptura_kgf": 74.45 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1195},
    "Parakeet": {"diametro_mm": 23.22, "area_secao_total_mm2": 318.9, "area_secao_al_mm2": 282.31, "area_secao_aco_mm2": 36.6, "peso_total_kgfm": 1.06801, "peso_al_kgfm": 0.78277, "peso_aco_kgfm": 0.28524, "modulo_elasticidade_kgfmm2": 74000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-05, "carga_ruptura_kgf": 85.83 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1023},
    "Rook": {"diametro_mm": 24.84, "area_secao_total_mm2": 364.95, "area_secao_al_mm2": 323.07, "area_secao_aco_mm2": 41.88, "peso_total_kgfm": 1.22223, "peso_al_kgfm": 0.8958, "peso_aco_kgfm": 0.32643, "modulo_elasticidade_kgfmm2": 74000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-05, "carga_ruptura_kgf": 98.22 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0894},
    "Flamingo": {"diametro_mm": 25.38, "area_secao_total_mm2": 380.99, "area_secao_al_mm2": 337.27, "area_secao_aco_mm2": 43.72, "peso_total_kgfm": 1.27595, "peso_al_kgfm": 0.93517, "peso_aco_kgfm": 0.34077, "modulo_elasticidade_kgfmm2": 74000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-05, "carga_ruptura_kgf": 102.54 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0856},
    "Stilt": {"diametro_mm": 26.32, "area_secao_total_mm2": 410.15, "area_secao_al_mm2": 363.27, "area_secao_aco_mm2": 46.88, "peso_total_kgfm": 1.37262, "peso_al_kgfm": 1.00725, "peso_aco_kgfm": 0.36537, "modulo_elasticidade_kgfmm2": 74000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-05, "carga_ruptura_kgf": 110.2 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0795},
    "Cuckoo": {"diametro_mm": 27.72, "area_secao_total_mm2": 454.49, "area_secao_al_mm2": 402.33, "area_secao_aco_mm2": 52.15, "peso_total_kgfm": 1.52208, "peso_al_kgfm": 1.11557, "peso_aco_kgfm": 0.40651, "modulo_elasticidade_kgfmm2": 74000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.89e-05, "carga_ruptura_kgf": 120.32 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0718},
    "Teal": {"diametro_mm": 25.24, "area_secao_total_mm2": 376.68, "area_secao_al_mm2": 307.06, "area_secao_aco_mm2": 69.62, "peso_total_kgfm": 1.39773, "peso_al_kgfm": 0.8527, "peso_aco_kgfm": 0.54503, "modulo_elasticidade_kgfmm2": 75000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.8e-05, "carga_ruptura_kgf": 128.55 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0943},
    "Egret": {"diametro_mm": 25.9, "area_secao_total_mm2": 396.11, "area_secao_al_mm2": 322.56, "area_secao_aco_mm2": 73.54, "peso_total_kgfm": 1.47147, "peso_al_kgfm": 0.89575, "peso_aco_kgfm": 0.57573, "modulo_elasticidade_kgfmm2": 75000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.8e-05, "carga_ruptura_kgf": 135.51 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0897},
    "Tern": {"diametro_mm": 27.03, "area_secao_total_mm2": 431.6, "area_secao_al_mm2": 403.77, "area_secao_aco_mm2": 27.83, "peso_total_kgfm": 1.33608, "peso_al_kgfm": 1.11874, "peso_aco_kgfm": 0.21734, "modulo_elasticidade_kgfmm2": 65000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.09e-05, "carga_ruptura_kgf": 96.33 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0715},
    "Ruddy": {"diametro_mm": 28.74, "area_secao_total_mm2": 487.17, "area_secao_al_mm2": 455.5, "area_secao_aco_mm2": 31.67, "peso_total_kgfm": 1.50936, "peso_al_kgfm": 1.26208, "peso_aco_kgfm": 0.24729, "modulo_elasticidade_kgfmm2": 65000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.09e-05, "carga_ruptura_kgf": 106.84 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0634},
    "Rail": {"diametro_mm": 29.61, "area_secao_total_mm2": 517.39, "area_secao_al_mm2": 483.84, "area_secao_aco_mm2": 33.54, "peso_total_kgfm": 1.60252, "peso_al_kgfm": 1.3406, "peso_aco_kgfm": 0.26192, "modulo_elasticidade_kgfmm2": 65000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.09e-05, "carga_ruptura_kgf": 113.37 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0597},
    "Ortolan": {"diametro_mm": 30.81, "area_secao_total_mm2": 560.18, "area_secao_al_mm2": 523.87, "area_secao_aco_mm2": 36.31, "peso_total_kgfm": 1.73506, "peso_al_kgfm": 1.4515, "peso_aco_kgfm": 0.28356, "modulo_elasticidade_kgfmm2": 65000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.09e-05, "carga_ruptura_kgf": 120.84 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0551},
    "Bluejay": {"diametro_mm": 31.98, "area_secao_total_mm2": 604.39, "area_secao_al_mm2": 565.49, "area_secao_aco_mm2": 38.9, "peso_total_kgfm": 1.87058, "peso_al_kgfm": 1.56681, "peso_aco_kgfm": 0.30377, "modulo_elasticidade_kgfmm2": 65000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.09e-05, "carga_ruptura_kgf": 130.09 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0511},
    "Bunting": {"diametro_mm": 33.12, "area_secao_total_mm2": 647.64, "area_secao_al_mm2": 605.76, "area_secao_aco_mm2": 41.88, "peso_total_kgfm": 2.00544, "peso_al_kgfm": 1.67841, "peso_aco_kgfm": 0.32704, "modulo_elasticidade_kgfmm2": 65000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.09e-05, "carga_ruptura_kgf": 139.6 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0477},
    "Bittern": {"diametro_mm": 34.17, "area_secao_total_mm2": 689.06, "area_secao_al_mm2": 644.4, "area_secao_aco_mm2": 44.66, "peso_total_kgfm": 2.13418, "peso_al_kgfm": 1.78547, "peso_aco_kgfm": 0.34871, "modulo_elasticidade_kgfmm2": 65000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.09e-05, "carga_ruptura_kgf": 148.63 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0448},
    "Bobolink": {"diametro_mm": 36.24, "area_secao_total_mm2": 775.41, "area_secao_al_mm2": 725.27, "area_secao_aco_mm2": 50.14, "peso_total_kgfm": 2.40108, "peso_al_kgfm": 2.00952, "peso_aco_kgfm": 0.39155, "modulo_elasticidade_kgfmm2": 65000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.09e-05, "carga_ruptura_kgf": 167.14 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0398},
    "Duck": {"diametro_mm": 24.21, "area_secao_total_mm2": 346.68, "area_secao_al_mm2": 306.89, "area_secao_aco_mm2": 39.78, "peso_total_kgfm": 1.16102, "peso_al_kgfm": 0.8504, "peso_aco_kgfm": 0.31062, "modulo_elasticidade_kgfmm2": 67000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.94e-05, "carga_ruptura_kgf": 96.2 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0941},
    "Cannary": {"diametro_mm": 29.52, "area_secao_total_mm2": 515.43, "area_secao_al_mm2": 456.28, "area_secao_aco_mm2": 59.15, "peso_total_kgfm": 1.72617, "peso_al_kgfm": 1.26435, "peso_aco_kgfm": 0.46182, "modulo_elasticidade_kgfmm2": 67000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.94e-05, "carga_ruptura_kgf": 137.85 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0633},
    "Finch": {"diametro_mm": 32.85, "area_secao_total_mm2": 636.6, "area_secao_al_mm2": 565.03, "area_secao_aco_mm2": 71.57, "peso_total_kgfm": 2.13324, "peso_al_kgfm": 1.57101, "peso_aco_kgfm": 0.56223, "modulo_elasticidade_kgfmm2": 70000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.96e-05, "carga_ruptura_kgf": 169.43 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0514},
    "Grackle": {"diametro_mm": 33.97, "area_secao_total_mm2": 679.68, "area_secao_al_mm2": 602.79, "area_secao_aco_mm2": 76.89, "peso_total_kgfm": 2.28005, "peso_al_kgfm": 1.676, "peso_aco_kgfm": 0.60405, "modulo_elasticidade_kgfmm2": 70000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.96e-05, "carga_ruptura_kgf": 181.38 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0481},
    "Pheasant": {"diametro_mm": 35.1, "area_secao_total_mm2": 726.79, "area_secao_al_mm2": 645.08, "area_secao_aco_mm2": 81.71, "peso_total_kgfm": 2.43548, "peso_al_kgfm": 1.79359, "peso_aco_kgfm": 0.64188, "modulo_elasticidade_kgfmm2": 70000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.96e-05, "carga_ruptura_kgf": 188.81 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.045},
    "Martin": {"diametro_mm": 36.17, "area_secao_total_mm2": 772.06, "area_secao_al_mm2": 685.39, "area_secao_aco_mm2": 86.67, "peso_total_kgfm": 2.58653, "peso_al_kgfm": 1.90567, "peso_aco_kgfm": 0.68086, "modulo_elasticidade_kgfmm2": 70000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.96e-05, "carga_ruptura_kgf": 200.44 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0423},
    "Plover": {"diametro_mm": 37.24, "area_secao_total_mm2": 818.7, "area_secao_al_mm2": 726.92, "area_secao_aco_mm2": 91.78, "peso_total_kgfm": 2.74213, "peso_al_kgfm": 2.02114, "peso_aco_kgfm": 0.72099, "modulo_elasticidade_kgfmm2": 70000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.96e-05, "carga_ruptura_kgf": 212.43 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0399},
    "Parrot": {"diametro_mm": 38.25, "area_secao_total_mm2": 863.09, "area_secao_al_mm2": 766.06, "area_secao_aco_mm2": 97.03, "peso_total_kgfm": 2.89223, "peso_al_kgfm": 2.12996, "peso_aco_kgfm": 0.76226, "modulo_elasticidade_kgfmm2": 70000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.96e-05, "carga_ruptura_kgf": 224.22 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0379},
    "Falcon": {"diametro_mm": 39.26, "area_secao_total_mm2": 908.66, "area_secao_al_mm2": 806.23, "area_secao_aco_mm2": 102.43, "peso_total_kgfm": 3.04633, "peso_al_kgfm": 2.24164, "peso_aco_kgfm": 0.80469, "modulo_elasticidade_kgfmm2": 70000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.96e-05, "carga_ruptura_kgf": 236.32 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.036},
    "Chukar": {"diametro_mm": 40.7, "area_secao_total_mm2": 976.72, "area_secao_al_mm2": 903.18, "area_secao_aco_mm2": 73.54, "peso_total_kgfm": 3.09013, "peso_al_kgfm": 2.5117, "peso_aco_kgfm": 0.57843, "modulo_elasticidade_kgfmm2": 70000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.96e-05, "carga_ruptura_kgf": 222.18 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0321},
    "Bluebird": {"diametro_mm": 44.76, "area_secao_total_mm2": 1181.69, "area_secao_al_mm2": 1092.84, "area_secao_aco_mm2": 88.84, "peso_total_kgfm": 3.73792, "peso_al_kgfm": 3.03916, "peso_aco_kgfm": 0.69876, "modulo_elasticidade_kgfmm2": 70000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.96e-05, "carga_ruptura_kgf": 262.26 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0266},
    "Kiwi": {"diametro_mm": 44.1, "area_secao_total_mm2": 1147.28, "area_secao_al_mm2": 1099.76, "area_secao_aco_mm2": 47.52, "peso_total_kgfm": 3.43303, "peso_al_kgfm": 3.06002, "peso_aco_kgfm": 0.37301, "modulo_elasticidade_kgfmm2": 70000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.96e-05, "carga_ruptura_kgf": 218.51 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0264},
    "Thrasher": {"diametro_mm": 45.79, "area_secao_total_mm2": 1235.36, "area_secao_al_mm2": 1171.42, "area_secao_aco_mm2": 63.94, "peso_total_kgfm": 3.76178, "peso_al_kgfm": 3.25866, "peso_aco_kgfm": 0.50312, "modulo_elasticidade_kgfmm2": 70000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.96e-05, "carga_ruptura_kgf": 247.69 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0248},
    "Grouse": {"diametro_mm": 9.32, "area_secao_total_mm2": 54.66, "area_secao_al_mm2": 40.54, "area_secao_aco_mm2": 14.12, "peso_total_kgfm": 0.22161, "peso_al_kgfm": 0.11218, "peso_aco_kgfm": 0.10943, "modulo_elasticidade_kgfmm2": 78000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.78e-05, "carga_ruptura_kgf": 22.15 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.7088},
    "Petrel": {"diametro_mm": 11.7, "area_secao_total_mm2": 81.71, "area_secao_al_mm2": 51.61, "area_secao_aco_mm2": 30.1, "peso_total_kgfm": 0.37812, "peso_al_kgfm": 0.14327, "peso_aco_kgfm": 0.23486, "modulo_elasticidade_kgfmm2": 78000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.78e-05, "carga_ruptura_kgf": 44.18 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.5595},
    "Minorca": {"diametro_mm": 12.2, "area_secao_total_mm2": 88.84, "area_secao_al_mm2": 56.11, "area_secao_aco_mm2": 32.73, "peso_total_kgfm": 0.41113, "peso_al_kgfm": 0.15577, "peso_aco_kgfm": 0.25536, "modulo_elasticidade_kgfmm2": 78000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.78e-05, "carga_ruptura_kgf": 48.04 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.5146},
    "Leghorn": {"diametro_mm": 13.45, "area_secao_total_mm2": 107.98, "area_secao_al_mm2": 68.2, "area_secao_aco_mm2": 39.78, "peso_total_kgfm": 0.4997, "peso_al_kgfm": 0.18933, "peso_aco_kgfm": 0.31037, "modulo_elasticidade_kgfmm2": 78000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.78e-05, "carga_ruptura_kgf": 57.93 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.423},
    "Guinea": {"diametro_mm": 14.6, "area_secao_total_mm2": 127.24, "area_secao_al_mm2": 80.36, "area_secao_aco_mm2": 46.88, "peso_total_kgfm": 0.5888, "peso_al_kgfm": 0.22309, "peso_aco_kgfm": 0.36571, "modulo_elasticidade_kgfmm2": 78000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.78e-05, "carga_ruptura_kgf": 68.03 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.3593},
    "Dotterel": {"diametro_mm": 15.4, "area_secao_total_mm2": 141.56, "area_secao_al_mm2": 89.41, "area_secao_aco_mm2": 52.15, "peso_total_kgfm": 0.65509, "peso_al_kgfm": 0.24821, "peso_aco_kgfm": 0.40689, "modulo_elasticidade_kgfmm2": 78000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.78e-05, "carga_ruptura_kgf": 73.34 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.323},
    "Dorking": {"diametro_mm": 16.0, "area_secao_total_mm2": 152.81, "area_secao_al_mm2": 96.51, "area_secao_aco_mm2": 56.3, "peso_total_kgfm": 0.70713, "peso_al_kgfm": 0.26792, "peso_aco_kgfm": 0.43921, "modulo_elasticidade_kgfmm2": 78000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.78e-05, "carga_ruptura_kgf": 79.17 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.2992},
    "Brahma": {"diametro_mm": 18.12, "area_secao_total_mm2": 194.57, "area_secao_al_mm2": 102.79, "area_secao_aco_mm2": 91.78, "peso_total_kgfm": 1.00311, "peso_al_kgfm": 0.2853, "peso_aco_kgfm": 0.71782, "modulo_elasticidade_kgfmm2": 75000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.8e-05, "carga_ruptura_kgf": 120.65 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.2809},
    "Cochin": {"diametro_mm": 16.85, "area_secao_total_mm2": 169.47, "area_secao_al_mm2": 107.04, "area_secao_aco_mm2": 62.44, "peso_total_kgfm": 0.78426, "peso_al_kgfm": 0.29715, "peso_aco_kgfm": 0.48712, "modulo_elasticidade_kgfmm2": 78000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 1.78e-05, "carga_ruptura_kgf": 87.8 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.2698}
}

# =============================================================
# Base de dados de cabos CA (Alumínio puro)
# Fonte: Catálogo Alubar 2015, Páginas 17-18
# =============================================================
CABOS_CA = {
    # Cabos com 7 fios: Módulo Elasticidade: 60 GPa, Coef. Dilatação: 23e-6 /°C
    "Peachbell": {"diametro_mm": 4.65, "area_secao_total_mm2": 13.21, "area_secao_al_mm2": 13.21, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.03642, "peso_al_kgfm": 0.03642, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 60000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 2.5 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 2.1754},
    "Rose": {"diametro_mm": 5.88, "area_secao_total_mm2": 21.12, "area_secao_al_mm2": 21.12, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.05823, "peso_al_kgfm": 0.05823, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 60000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 3.91 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 1.3605},
    "Lily": {"diametro_mm": 6.6, "area_secao_total_mm2": 26.61, "area_secao_al_mm2": 26.61, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.07336, "peso_al_kgfm": 0.07336, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 60000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 4.85 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 1.0798},
    "Iris": {"diametro_mm": 7.41, "area_secao_total_mm2": 33.54, "area_secao_al_mm2": 33.54, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.09248, "peso_al_kgfm": 0.09248, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 60000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 5.99 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.8567},
    "Pansy": {"diametro_mm": 8.34, "area_secao_total_mm2": 42.49, "area_secao_al_mm2": 42.49, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.11714, "peso_al_kgfm": 0.11714, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 60000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 7.3 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.6763},
    "Poppy": {"diametro_mm": 9.36, "area_secao_total_mm2": 53.52, "area_secao_al_mm2": 53.52, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.14755, "peso_al_kgfm": 0.14755, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 60000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 8.84 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.5369},
    "Aster": {"diametro_mm": 10.5, "area_secao_total_mm2": 67.35, "area_secao_al_mm2": 67.35, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.18568, "peso_al_kgfm": 0.18568, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 60000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 11.12 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.4266},
    "Phlox": {"diametro_mm": 11.79, "area_secao_total_mm2": 84.91, "area_secao_al_mm2": 84.91, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.23411, "peso_al_kgfm": 0.23411, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 60000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 13.45 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.3384},
    "Oxlip": {"diametro_mm": 13.26, "area_secao_total_mm2": 107.41, "area_secao_al_mm2": 107.41, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.29613, "peso_al_kgfm": 0.29613, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 60000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 17.01 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.2675},
    "Sneezewort": {"diametro_mm": 14.4, "area_secao_total_mm2": 126.67, "area_secao_al_mm2": 126.67, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.34923, "peso_al_kgfm": 0.34923, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 60000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 20.06 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.2268},
    "Daisy": {"diametro_mm": 14.88, "area_secao_total_mm2": 135.25, "area_secao_al_mm2": 135.25, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.3729, "peso_al_kgfm": 0.3729, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 60000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 21.42 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.2124},
    # Cabos com 19 fios: Módulo Elasticidade: 57 GPa, Coef. Dilatação: 23e-6 /°C
    "Valerian": {"diametro_mm": 14.55, "area_secao_total_mm2": 126.37, "area_secao_al_mm2": 126.37, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.3484, "peso_al_kgfm": 0.3484, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 20.68 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.2274},
    "Laurel": {"diametro_mm": 15.05, "area_secao_total_mm2": 135.2, "area_secao_al_mm2": 135.2, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.37275, "peso_al_kgfm": 0.37275, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 22.13 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.2125},
    "Peony": {"diametro_mm": 15.95, "area_secao_total_mm2": 151.85, "area_secao_al_mm2": 151.85, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.41867, "peso_al_kgfm": 0.41867, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 24.29 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1892},
    "Tulip": {"diametro_mm": 16.9, "area_secao_total_mm2": 170.48, "area_secao_al_mm2": 170.48, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.47003, "peso_al_kgfm": 0.47003, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 27.27 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1685},
    "Daffodil": {"diametro_mm": 17.25, "area_secao_total_mm2": 177.62, "area_secao_al_mm2": 177.62, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.4897, "peso_al_kgfm": 0.4897, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 28.41 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1618},
    "Canna": {"diametro_mm": 18.4, "area_secao_total_mm2": 202.09, "area_secao_al_mm2": 202.09, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.55717, "peso_al_kgfm": 0.55717, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 31.76 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1422},
    "Goldentuft": {"diametro_mm": 19.55, "area_secao_total_mm2": 228.14, "area_secao_al_mm2": 228.14, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.62899, "peso_al_kgfm": 0.62899, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 35.01 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1259},
    "Cosmos": {"diametro_mm": 20.1, "area_secao_total_mm2": 241.15, "area_secao_al_mm2": 241.15, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.66488, "peso_al_kgfm": 0.66488, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 37.01 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1191},
    "Zinnia": {"diametro_mm": 20.6, "area_secao_total_mm2": 253.3, "area_secao_al_mm2": 253.3, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.69837, "peso_al_kgfm": 0.69837, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 38.87 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1134},
    "Dahlia": {"diametro_mm": 21.75, "area_secao_total_mm2": 282.37, "area_secao_al_mm2": 282.37, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.77852, "peso_al_kgfm": 0.77852, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 43.33 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1022},
    # Cabos com 37 fios: Módulo Elasticidade: 57 GPa, Coef. Dilatação: 23e-6 /°C
    "Syringa": {"diametro_mm": 20.16, "area_secao_total_mm2": 241.03, "area_secao_al_mm2": 241.03, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.66454, "peso_al_kgfm": 0.66454, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 38.6 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1192},
    "Hyacinth": {"diametro_mm": 20.65, "area_secao_total_mm2": 252.89, "area_secao_al_mm2": 252.89, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.69724, "peso_al_kgfm": 0.69724, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 40.5 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1136},
    "Mistietoe": {"diametro_mm": 21.77, "area_secao_total_mm2": 281.07, "area_secao_al_mm2": 281.07, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.77492, "peso_al_kgfm": 0.77492, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 43.99 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.1022},
    "Meadowsweet": {"diametro_mm": 22.61, "area_secao_total_mm2": 303.18, "area_secao_al_mm2": 303.18, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.83588, "peso_al_kgfm": 0.83588, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 47.45 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0948},
    "Orchid": {"diametro_mm": 23.31, "area_secao_total_mm2": 322.24, "area_secao_al_mm2": 322.24, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.88844, "peso_al_kgfm": 0.88844, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 50.44 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0892},
    "Heuchera": {"diametro_mm": 23.59, "area_secao_total_mm2": 330.03, "area_secao_al_mm2": 330.03, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.90991, "peso_al_kgfm": 0.90991, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 51.66 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0871},
    "Verbena": {"diametro_mm": 24.43, "area_secao_total_mm2": 353.95, "area_secao_al_mm2": 353.95, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.97586, "peso_al_kgfm": 0.97586, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 55.4 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0812},
    "Violet": {"diametro_mm": 24.71, "area_secao_total_mm2": 362.11, "area_secao_al_mm2": 362.11, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.99836, "peso_al_kgfm": 0.99836, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 56.68 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0793},
    "Petunia": {"diametro_mm": 25.34, "area_secao_total_mm2": 380.81, "area_secao_al_mm2": 380.81, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.04992, "peso_al_kgfm": 1.04992, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 58.56 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0755},
    "Arbutus": {"diametro_mm": 26.04, "area_secao_total_mm2": 402.14, "area_secao_al_mm2": 402.14, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.10872, "peso_al_kgfm": 1.10872, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 61.85 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0715},
    "Anemone": {"diametro_mm": 27.37, "area_secao_total_mm2": 444.27, "area_secao_al_mm2": 444.27, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.22487, "peso_al_kgfm": 1.22487, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 66.71 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0647},
    "Cockscomb": {"diametro_mm": 27.72, "area_secao_total_mm2": 455.7, "area_secao_al_mm2": 455.7, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.2564, "peso_al_kgfm": 1.2564, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 68.42 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0631},
    "Magnolia": {"diametro_mm": 28.56, "area_secao_total_mm2": 483.74, "area_secao_al_mm2": 483.74, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.3337, "peso_al_kgfm": 1.3337, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 72.63 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0594},
    "Hawkweed": {"diametro_mm": 29.26, "area_secao_total_mm2": 507.74, "area_secao_al_mm2": 507.74, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.39988, "peso_al_kgfm": 1.39988, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 76.24 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0566},
    "Bluebell": {"diametro_mm": 29.68, "area_secao_total_mm2": 522.42, "area_secao_al_mm2": 522.42, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.44035, "peso_al_kgfm": 1.44035, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 57000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 78.44 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.055},
    # Cabos com 61 fios: Módulo Elasticidade: 55 GPa, Coef. Dilatação: 23e-6 /°C
    "Flag": {"diametro_mm": 24.48, "area_secao_total_mm2": 354.45, "area_secao_al_mm2": 354.45, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.97725, "peso_al_kgfm": 0.97725, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 57.1 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0811},
    "Nasturtium": {"diametro_mm": 24.75, "area_secao_total_mm2": 362.31, "area_secao_al_mm2": 362.31, "area_secao_aco_mm2": 0, "peso_total_kgfm": 0.99892, "peso_al_kgfm": 0.99892, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 58.37 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0793},
    "Cattail": {"diametro_mm": 25.38, "area_secao_total_mm2": 380.99, "area_secao_al_mm2": 380.99, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.05042, "peso_al_kgfm": 1.05042, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 60.35 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0754},
    "Lilac": {"diametro_mm": 26.1, "area_secao_total_mm2": 402.92, "area_secao_al_mm2": 402.92, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.11087, "peso_al_kgfm": 1.11087, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 63.82 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0713},
    "Snapdragon": {"diametro_mm": 27.81, "area_secao_total_mm2": 457.44, "area_secao_al_mm2": 457.44, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.2612, "peso_al_kgfm": 1.2612, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 70.81 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0628},
    "Goldenrod": {"diametro_mm": 28.62, "area_secao_total_mm2": 484.48, "area_secao_al_mm2": 484.48, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.33573, "peso_al_kgfm": 1.33573, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 75.0 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0593},
    "Camellia": {"diametro_mm": 29.25, "area_secao_total_mm2": 506.04, "area_secao_al_mm2": 506.04, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.39519, "peso_al_kgfm": 1.39519, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 78.34 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0568},
    "Larkspur": {"diametro_mm": 29.79, "area_secao_total_mm2": 524.9, "area_secao_al_mm2": 524.9, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.44718, "peso_al_kgfm": 1.44718, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 81.25 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0547},
    "Marigold": {"diametro_mm": 30.87, "area_secao_total_mm2": 563.65, "area_secao_al_mm2": 563.65, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.55401, "peso_al_kgfm": 1.55401, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 87.25 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.051},
    "Hawthorn": {"diametro_mm": 31.95, "area_secao_total_mm2": 603.78, "area_secao_al_mm2": 603.78, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.66465, "peso_al_kgfm": 1.66465, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 93.46 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0476},
    "Narcissus": {"diametro_mm": 33.03, "area_secao_total_mm2": 645.29, "area_secao_al_mm2": 645.29, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.77909, "peso_al_kgfm": 1.77909, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 98.15 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0445},
    "Columbine": {"diametro_mm": 34.02, "area_secao_total_mm2": 684.55, "area_secao_al_mm2": 684.55, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.88734, "peso_al_kgfm": 1.88734, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 104.12 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.042},
    "Carnation": {"diametro_mm": 35.01, "area_secao_total_mm2": 724.97, "area_secao_al_mm2": 724.97, "area_secao_aco_mm2": 0, "peso_total_kgfm": 1.99878, "peso_al_kgfm": 1.99878, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 107.66 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0396},
    "Gladiolus": {"diametro_mm": 36.0, "area_secao_total_mm2": 766.55, "area_secao_al_mm2": 766.55, "area_secao_aco_mm2": 0, "peso_total_kgfm": 2.11342, "peso_al_kgfm": 2.11342, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 113.83 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0375},
    "Coreopsis": {"diametro_mm": 36.9, "area_secao_total_mm2": 805.36, "area_secao_al_mm2": 805.36, "area_secao_aco_mm2": 0, "peso_total_kgfm": 2.22041, "peso_al_kgfm": 2.22041, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 119.6 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0357},
    "Jessamine": {"diametro_mm": 38.7, "area_secao_total_mm2": 885.84, "area_secao_al_mm2": 885.84, "area_secao_aco_mm2": 0, "peso_total_kgfm": 2.44232, "peso_al_kgfm": 2.44232, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 55000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 131.55 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0324},
    # Cabos com 91 fios: Módulo Elasticidade: 54 GPa, Coef. Dilatação: 23e-6 /°C
    "Cowslip": {"diametro_mm": 41.36, "area_secao_total_mm2": 1010.43, "area_secao_al_mm2": 1010.43, "area_secao_aco_mm2": 0, "peso_total_kgfm": 2.81313, "peso_al_kgfm": 2.81313, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 54000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 151.98 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0287},
    "Sagebrush": {"diametro_mm": 43.89, "area_secao_total_mm2": 1137.83, "area_secao_al_mm2": 1137.83, "area_secao_aco_mm2": 0, "peso_total_kgfm": 3.16782, "peso_al_kgfm": 3.16782, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 54000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 167.09 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0255},
    "Lupine": {"diametro_mm": 46.31, "area_secao_total_mm2": 1266.76, "area_secao_al_mm2": 1266.76, "area_secao_aco_mm2": 0, "peso_total_kgfm": 3.52678, "peso_al_kgfm": 3.52678, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 54000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 186.02 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0229},
    "Bitteroot": {"diametro_mm": 48.62, "area_secao_total_mm2": 1396.29, "area_secao_al_mm2": 1396.29, "area_secao_aco_mm2": 0, "peso_total_kgfm": 3.8874, "peso_al_kgfm": 3.8874, "peso_aco_kgfm": 0, "modulo_elasticidade_kgfmm2": 54000 * MPA_PARA_KGFMM2, "coef_dilatacao_termica_1porc": 2.3e-05, "carga_ruptura_kgf": 205.05 * KN_PARA_KGF, "resistencia_eletrica_20c_ohm_km": 0.0208}
}

CABOS_CAL = {
    # AAAC - ASTM B399M
    "Ames": {
        "area_mm2": 77.47,
        "formacao": "7 x 2,67",
        "diametro_mm": 8.01,
        "massa_linear_kg_km": 107.54,
        "rmc_kN": 12.45,
        "resistencia_20C_ohm_km": 0.8547,
        "ampacidade_75C_A": 214,
    },
    "Azusa": {
        "area_mm2": 123.3,
        "formacao": "7 x 3,37",
        "diametro_mm": 10.11,
        "massa_linear_kg_km": 171.32,
        "rmc_kN": 19.00,
        "resistencia_20C_ohm_km": 0.5365,
        "ampacidade_75C_A": 287,
    },
    "Anaheim": {
        "area_mm2": 155.4,
        "formacao": "7 x 3,78",
        "diametro_mm": 11.34,
        "massa_linear_kg_km": 215.54,
        "rmc_kN": 23.91,
        "resistencia_20C_ohm_km": 0.4264,
        "ampacidade_75C_A": 331,
    },
    "Amherst": {
        "area_mm2": 195.7,
        "formacao": "7 x 4,25",
        "diametro_mm": 12.75,
        "massa_linear_kg_km": 272.47,
        "rmc_kN": 30.22,
        "resistencia_20C_ohm_km": 0.3373,
        "ampacidade_75C_A": 384,
    },
    "Alliance": {
        "area_mm2": 246.9,
        "formacao": "7 x 4,77",
        "diametro_mm": 14.31,
        "massa_linear_kg_km": 343.22,
        "rmc_kN": 38.07,
        "resistencia_20C_ohm_km": 0.2678,
        "ampacidade_75C_A": 444,
    },
    "Butte": {
        "area_mm2": 312.8,
        "formacao": "19 x 3,26",
        "diametro_mm": 16.30,
        "massa_linear_kg_km": 435.14,
        "rmc_kN": 46.75,
        "resistencia_20C_ohm_km": 0.2112,
        "ampacidade_75C_A": 516,
    },
    "Canton": {
        "area_mm2": 394.5,
        "formacao": "19 x 3,66",
        "diametro_mm": 18.30,
        "massa_linear_kg_km": 548.48,
        "rmc_kN": 58.93,
        "resistencia_20C_ohm_km": 0.1676,
        "ampacidade_75C_A": 597,
    },
    "Cairo": {
        "area_mm2": 465.4,
        "formacao": "19 x 3,98",
        "diametro_mm": 19.90,
        "massa_linear_kg_km": 648.58,
        "rmc_kN": 69.69,
        "resistencia_20C_ohm_km": 0.1417,
        "ampacidade_75C_A": 663,
    },
    "Darien": {
        "area_mm2": 559.5,
        "formacao": "19 x 4,36",
        "diametro_mm": 21.80,
        "massa_linear_kg_km": 778.34,
        "rmc_kN": 83.63,
        "resistencia_20C_ohm_km": 0.1181,
        "ampacidade_75C_A": 743,
    },
    "Elgin": {
        "area_mm2": 652.4,
        "formacao": "19 x 4,71",
        "diametro_mm": 23.55,
        "massa_linear_kg_km": 908.32,
        "rmc_kN": 97.59,
        "resistencia_20C_ohm_km": 0.1012,
        "ampacidade_75C_A": 818,
    },
    "Flint": {
        "area_mm2": 740.8,
        "formacao": "37 x 3,59",
        "diametro_mm": 25.13,
        "massa_linear_kg_km": 1027.62,
        "rmc_kN": 108.04,
        "resistencia_20C_ohm_km": 0.0894,
        "ampacidade_75C_A": 884,
    },
    "Greeley": {
        "area_mm2": 927.2,
        "formacao": "37 x 4,02",
        "diametro_mm": 28.14,
        "massa_linear_kg_km": 1288.53,
        "rmc_kN": 135.47,
        "resistencia_20C_ohm_km": 0.0713,
        "ampacidade_75C_A": 1016,
    },
    # Se quiser, mantenho também os tamanhos sem “nome” da mesma tabela:
    "1077.4 MCM": {
        "area_mm2": 547.33,
        "formacao": "61 x 3,38",
        "diametro_mm": 30.42,
        "massa_linear_kg_km": 1501.78,
        "rmc_kN": 156.15,
        "resistencia_20C_ohm_km": 0.0612,
        "ampacidade_75C_A": 1116,
    },
    "1165.1 MCM": {
        "area_mm2": 590.25,
        "formacao": "61 x 3,51",
        "diametro_mm": 31.59,
        "massa_linear_kg_km": 1619.52,
        "rmc_kN": 168.40,
        "resistencia_20C_ohm_km": 0.0568,
        "ampacidade_75C_A": 1169,
    },
    "1259.6 MCM": {
        "area_mm2": 638.27,
        "formacao": "61 x 3,65",
        "diametro_mm": 32.85,
        "massa_linear_kg_km": 1751.29,
        "rmc_kN": 182.10,
        "resistencia_20C_ohm_km": 0.0525,
        "ampacidade_75C_A": 1226,
    },
}

# =============================================================
# Base de dados de cabos para-raios (aço galvanizado)
# NOTA: Estes dados não foram encontrados no catálogo fornecido
# e foram mantidos do código original.
# =============================================================
CABOS_PARA_RAIOS = {
    "EHS_38": {
        "diametro_mm": 7.9,
        "area_secao_total_mm2": 37.9,
        "peso_total_kgfm": 0.298,
        "modulo_elasticidade_kgfmm2": 16500.0, # Valor típico para aço
        "coef_dilatacao_termica_1porc": 1.15e-5, # Valor típico para aço
        "carga_ruptura_kgf": 3450.0
    },
    # Outros cabos para-raios poderiam ser adicionados aqui
}


# =============================================================
# Dicionário unificado e funções factory
# =============================================================

# Unifica todos os dicionários de cabos em um só
_BD_CABOS = {**CABOS_CAA, **CABOS_CA, **CABOS_PARA_RAIOS, **CABOS_CAL}


def criar_cabo(nome_cabo: str) -> Optional[Cabo]:
    """
    Cria uma instância da classe Cabo a partir do nome do cabo.

    Busca os dados do cabo no banco de dados interno e, se encontrado,
    retorna um objeto Cabo inicializado com esses dados.

    Args:
        nome_cabo: O nome do cabo (ex: "Linnet", "Daisy").

    Returns:
        Uma instância da classe Cabo se o nome for encontrado,
        caso contrário, retorna None.
    """
    dados_cabo = _BD_CABOS.get(nome_cabo)

    if dados_cabo:
        # A criação da instância da classe Cabo depende da sua definição
        # no módulo 'elementos'. Exemplo de como poderia ser:
        # return Cabo(nome=nome_cabo, **dados_cabo)
        print(f"Dados para o cabo '{nome_cabo}': {dados_cabo}")
        return dados_cabo  # Retornando o dicionário por enquanto
    else:
        print(f"Cabo com nome '{nome_cabo}' não encontrado na base de dados.")
        return None


def listar_cabos() -> List[str]:
    """
    Retorna uma lista com os nomes de todos os cabos disponíveis.

    Returns:
        Uma lista de strings com os nomes dos cabos.
    """
    return list(_BD_CABOS.keys())

# Exemplo de uso:
if __name__ == '__main__':
    # Listar todos os cabos disponíveis
    print("Cabos disponíveis:")
    lista_de_cabos = sorted(listar_cabos())
    print(lista_de_cabos)
    print("-" * 30)

    # Criar e exibir dados de um cabo CAA
    print("Testando cabo CAA 'Linnet':")
    cabo_linnet = criar_cabo("Linnet")
    if cabo_linnet:
        # Aqui você usaria os atributos do objeto Cabo, por exemplo:
        # print(f"Diâmetro: {cabo_linnet.diametro_mm} mm")
        # print(f"Carga de Ruptura: {cabo_linnet.carga_ruptura_kgf:.2f} kgf")
        pass # Apenas o print dentro da função será executado por enquanto
    print("-" * 30)

    # Criar e exibir dados de um cabo CA
    print("Testando cabo CA 'Daisy':")
    cabo_daisy = criar_cabo("Daisy")
    if cabo_daisy:
        pass
    print("-" * 30)

    # Tentar criar um cabo inexistente
    print("Testando cabo inexistente:")
    cabo_inexistente = criar_cabo("CaboInexistente")

