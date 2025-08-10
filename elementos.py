from __future__ import annotations
"""
Módulo: elementos.py

Este módulo define as classes para os componentes físicos de uma linha de
transmissão, como Cabos, Isoladores, etc. O objetivo é encapsular
as propriedades e os cálculos intrínsecos de cada elemento.
"""

import math
from dataclasses import dataclass, field
from typing import Optional

# Assumindo que o arquivo mec_5422.py está no mesmo diretório ou em um
# local acessível pelo Python.
from mec_5422 import CalculadoraNBR5422


@dataclass(frozen=True, slots=True)
class Cabo:
    """
    Representa um cabo condutor ou para-raios, encapsulando suas
    propriedades mecânicas e físicas.

    As propriedades são fornecidas em unidades comuns de catálogo (mm, kgf/m, etc.)
    e são automaticamente convertidas para o Sistema Internacional (SI) para
    uso nos cálculos, garantindo consistência.
    """
    # --- Propriedades de Catálogo (Entrada) ---
    nome: str
    diametro_mm: float
    area_secao_mm2: float
    peso_kgfm: float
    modulo_elasticidade_kgfmm2: float
    coef_dilatacao_termica_1porc: float
    carga_ruptura_kgf: float

    # --- Propriedades Calculadas (SI) ---
    # Estes campos são inicializados no __post_init__
    diametro_m: float = field(init=False)
    area_secao_m2: float = field(init=False)
    peso_unit_npm: float = field(init=False)  # N/m (Newton por metro)
    modulo_elasticidade_pa: float = field(init=False) # Pa (Pascal)
    carga_ruptura_n: float = field(init=False) # N (Newton)

    def __post_init__(self) -> None:
        """
        Valida os dados de entrada e calcula as propriedades em unidades do SI
        após a inicialização do objeto.
        """
        # --- Validações ---
        if self.diametro_mm <= 0:
            raise ValueError("O diâmetro deve ser positivo.")
        if self.area_secao_mm2 <= 0:
            raise ValueError("A área da seção deve ser positiva.")
        if self.peso_kgfm <= 0:
            raise ValueError("O peso deve ser positivo.")
        if self.carga_ruptura_kgf <= 0:
            raise ValueError("A carga de ruptura deve ser positiva.")
        if self.modulo_elasticidade_kgfmm2 <= 0:
            raise ValueError("O módulo de elasticidade deve ser positivo.")

        # --- Conversões para o Sistema Internacional (SI) ---
        g = CalculadoraNBR5422.ACELERACAO_GRAVIDADE  # 9.80665 m/s²

        # Usamos object.__setattr__ pois o dataclass é frozen (imutável)
        object.__setattr__(self, 'diametro_m', self.diametro_mm / 1000.0)
        object.__setattr__(self, 'area_secao_m2', self.area_secao_mm2 / 1_000_000.0)
        object.__setattr__(self, 'peso_unit_npm', self.peso_kgfm * g)
        object.__setattr__(self, 'carga_ruptura_n', self.carga_ruptura_kgf * g)
        # kgf/mm² para Pa (N/m²): (kgf/mm²) * (g N/kgf) * (1e6 mm²/m²)
        object.__setattr__(
            self,
            'modulo_elasticidade_pa',
            self.modulo_elasticidade_kgfmm2 * g * 1_000_000.0
        )

    @property
    def coef_arrasto(self) -> float:
        """
        Calcula o coeficiente de arrasto (Cx) do cabo com base no seu diâmetro.

        Retorna:
            float: Coeficiente de arrasto (1.2 para d < 15mm, 1.0 caso contrário).
        """
        return CalculadoraNBR5422.coef_arrasto_cabo(self.diametro_m)

    def peso_resultante_npm(self, forca_vento_horizontal_npm: float) -> float:
        """
        Calcula o peso unitário resultante (vetorial) combinando o peso
        próprio do cabo com uma força de vento horizontal por metro.

        Args:
            forca_vento_horizontal_npm (float): Força do vento por metro (N/m).

        Returns:
            float: Peso unitário resultante (N/m).
        """
        if forca_vento_horizontal_npm < 0:
            raise ValueError("Força de vento deve ser não negativa.")
        return math.hypot(self.peso_unit_npm, forca_vento_horizontal_npm)

    def __repr__(self) -> str:
        return (
            f"Cabo(nome='{self.nome}', "
            f"diametro={self.diametro_mm} mm, "
            f"peso={self.peso_kgfm} kgf/m, "
            f"RTS={self.carga_ruptura_kgf:,.0f} kgf)"
        )


# =============================================================
# Exemplo de uso
# =============================================================

if __name__ == "__main__":
    print("=== Exemplo de Instanciação da Classe Cabo ===")

    # Dados de um cabo típico (ex: Linnet), baseados no seu script antigo
    try:
        cabo_linnet = Cabo(
            nome="Linnet",
            diametro_mm=18.1,
            area_secao_mm2=203.0,
            peso_kgfm=0.704,
            modulo_elasticidade_kgfmm2=8010.0,
            coef_dilatacao_termica_1porc=1.93e-5,
            carga_ruptura_kgf=7348.0
        )

        print(f"\nObjeto criado: {cabo_linnet}")

        print("\n--- Propriedades de Entrada (Unidades de Catálogo) ---")
        print(f"Nome: {cabo_linnet.nome}")
        print(f"Diâmetro: {cabo_linnet.diametro_mm} mm")
        print(f"Área: {cabo_linnet.area_secao_mm2} mm²")
        print(f"Peso: {cabo_linnet.peso_kgfm} kgf/m")
        print(f"Módulo Elasticidade: {cabo_linnet.modulo_elasticidade_kgfmm2} kgf/mm²")
        print(f"Ruptura: {cabo_linnet.carga_ruptura_kgf:,.1f} kgf")


        print("\n--- Propriedades Convertidas (Unidades SI) ---")
        print(f"Diâmetro: {cabo_linnet.diametro_m:.4f} m")
        print(f"Área: {cabo_linnet.area_secao_m2:.4e} m²")
        print(f"Peso Unitário: {cabo_linnet.peso_unit_npm:.2f} N/m")
        print(f"Módulo Elasticidade: {cabo_linnet.modulo_elasticidade_pa / 1e9:.2f} GPa")
        print(f"Ruptura: {cabo_linnet.carga_ruptura_n / 1000:.2f} kN")

        print("\n--- Métodos Auxiliares ---")
        print(f"Coeficiente de Arrasto (Cx): {cabo_linnet.coef_arrasto}")

        # Exemplo de cálculo de peso resultante com vento
        pressao_dinamica = 600.0  # Pa (exemplo)
        forca_vento_por_metro = pressao_dinamica * cabo_linnet.coef_arrasto * cabo_linnet.diametro_m
        peso_res = cabo_linnet.peso_resultante_npm(forca_vento_por_metro)
        print(f"Com q₀={pressao_dinamica:.1f} Pa, a força de vento é {forca_vento_por_metro:.2f} N/m")
        print(f"Peso resultante (próprio + vento): {peso_res:.2f} N/m")


    except Exception as e:
        print(f"\nErro ao criar o objeto Cabo: {e}")