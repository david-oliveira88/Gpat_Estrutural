from __future__ import annotations
"""
Módulo: mec_5422.py

Refatorado para facilitar a criação e iteração sobre N casos de carga.
- Defina uma vez o ambiente padrão (altitude/tipo de terreno).
- Modele os cenários com CasoDeCarga.
- Use CasosDeCarga para iterar, gerar combinações e calcular forças.

Observação importante: ajuste coeficientes/tabelas conforme sua leitura da NBR 5422:2024.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Tuple, Union, Callable, Any
import math
import itertools
import time



# =============================================================
# Enumerações e estruturas básicas
# =============================================================

class TipoTerreno(Enum):
    """Categorias de terreno conforme tipificação usual em NBR 5422."""
    A = "A"  # água/planícies
    B = "B"  # aberto, poucos obstáculos
    C = "C"  # obstáculos pequenos e numerosos
    D = "D"  # urbano/denso, árvores altas


@dataclass(frozen=True, slots=True)
class ParametrosTerreno:
    gc_a: float
    gc_b: float
    gt_a: float
    gt_b: float
    gt_c: float


# =============================================================
# Ambiente padrão (singleton simples)
# =============================================================

class AmbientePadrao:
    """Armazena valores padrão do projeto (defina uma vez com set_defaults)."""
    altitude_m: float = 0.0
    tipo_terreno: TipoTerreno = TipoTerreno.B

    @classmethod
    def set_defaults(cls, *, altitude_m: float, tipo_terreno: Union[TipoTerreno, str]) -> None:
        if altitude_m < 0:
            raise ValueError("altitude_m deve ser não negativa.")
        if isinstance(tipo_terreno, str):
            try:
                tipo_terreno = TipoTerreno[tipo_terreno.upper()]
            except KeyError as e:
                raise ValueError("tipo_terreno deve ser 'A', 'B', 'C' ou 'D'.") from e
        cls.altitude_m = float(altitude_m)
        cls.tipo_terreno = tipo_terreno


# =============================================================
# Núcleo de cálculos
# =============================================================

class CalculadoraNBR5422:
    """Rotinas de cálculo auxiliares (ajuste constantes conforme seu procedimento)."""
    # Constantes
    ALTURA_MINIMA_CALCULO = 10.0  # m
    PRECISAO_MUDANCA_ESTADO = 1e-4
    MAX_ITERACOES = 10000
    DELTA_DERIVADA = 1.0
    COEF_ARRASTO_ISOLADOR = 1.2
    MASSA_AR_REFERENCIA = 1.225      # kg/m³ (15°C ao nível do mar)
    TEMP_REFERENCIA = 288.15         # K (15°C)
    ACELERACAO_GRAVIDADE = 9.80665   # m/s²

    # Parâmetros por tipo de terreno (exemplo; alinhar com sua base)
    PARAMETROS_TERRENO: Dict[TipoTerreno, ParametrosTerreno] = {
        TipoTerreno.A: ParametrosTerreno(0.2914, 1.0468, -0.0002, 0.0232, 1.4661),
        TipoTerreno.B: ParametrosTerreno(0.3733, 0.9762, -0.0002, 0.0274, 1.6820),
        TipoTerreno.C: ParametrosTerreno(0.4936, 0.9124, -0.0002, 0.0298, 2.2744),
        TipoTerreno.D: ParametrosTerreno(0.6153, 0.8144, -0.0002, 0.0384, 2.9284),
    }

    # ------------------------ Atmosfera ------------------------
    @classmethod
    def calcular_pressao_padrao(cls, altitude_m: float) -> float:
        """Pressão atmosférica padrão aproximada (Pa) pela fórmula barométrica simples."""
        # Altura de escala ~ 8434 m (isotérmico simplificado)
        p0 = 101_325.0
        H = 8434.0
        return float(p0 * math.exp(-max(0.0, altitude_m) / H))

    @classmethod
    def calcular_massa_especifica_ar(cls, temperatura_celsius: float, altitude_m: float) -> float:
        """
        Massa específica do ar (kg/m³). Aproximação comum em projetos.
        ρ ≈ ρ0 * (T0/T) * exp(-k * h)
        """
        temp_k = temperatura_celsius + 273.15
        rho = cls.MASSA_AR_REFERENCIA * (cls.TEMP_REFERENCIA / temp_k) * math.exp(-1.2e-4 * max(0.0, altitude_m))
        return float(round(rho, 3))

    @classmethod
    def calcular_densidade_relativa_ar(
        cls, pressao_pa: float, temperatura_celsius: float, p_ref: float = 101_325.0, t_ref_c: float = 20.0
    ) -> float:
        """Densidade relativa do ar (adimensional) ≈ (p/p0)*(T0/T)."""
        t_k = temperatura_celsius + 273.15
        t0_k = t_ref_c + 273.15
        dens_rel = (pressao_pa / p_ref) * (t0_k / t_k)
        return float(round(dens_rel, 6))

    @classmethod
    def calcular_pressao_dinamica(cls, massa_especifica: float, velocidade_vento: float) -> float:
        """Pressão dinâmica q = 0,5 * ρ * V² (Pa)."""
        if velocidade_vento < 0:
            raise ValueError("Velocidade do vento deve ser não negativa.")
        q = 0.5 * massa_especifica * (velocidade_vento ** 2)
        return float(round(q, 2))

    # -------------------- Fatores de vento ---------------------
    @classmethod
    def calcular_gc(cls, altura_m: float, tipo_terreno: TipoTerreno) -> float:
        """Fator combinado de vento GC para cabos."""
        if altura_m < 0:
            raise ValueError("Altura deve ser não negativa.")
        h = max(altura_m, cls.ALTURA_MINIMA_CALCULO)
        p = cls.PARAMETROS_TERRENO[tipo_terreno]
        gc = p.gc_a * math.log(h) + p.gc_b
        return float(round(gc, 4))

    @classmethod
    def calcular_gl(cls, comprimento_vao_m: float) -> float:
        """Fator de efetividade GL (polinômio segmentado)."""
        if comprimento_vao_m < 0:
            raise ValueError("Comprimento do vão deve ser não negativo.")
        L = comprimento_vao_m
        if L < 200:
            return 1.0
        if L < 800:
            return 1.693e-10 * L ** 3 - 1.093e-7 * L ** 2 - 2.686e-4 * L + 1.057
        return 0.858

    @classmethod
    def calcular_gt(cls, altura_m: float, tipo_terreno: TipoTerreno) -> float:
        """Fator combinado de vento GT para suportes/isoladores."""
        if altura_m < 0:
            raise ValueError("Altura deve ser não negativa.")
        h = max(altura_m, cls.ALTURA_MINIMA_CALCULO)
        p = cls.PARAMETROS_TERRENO[tipo_terreno]
        gt = p.gt_a * (h ** 2) + p.gt_b * h + p.gt_c
        return float(round(gt, 4))

    # ----------------------- Ações de vento --------------------
    @staticmethod
    def coef_arrasto_cabo(diametro_m: float) -> float:
        """Coeficiente de arrasto para cabo: 1.2 se d < 15 mm; caso contrário 1.0."""
        if diametro_m <= 0:
            raise ValueError("Diâmetro deve ser positivo.")
        return 1.2 if diametro_m < 0.015 else 1.0

    @classmethod
    def forca_vento_em_isolador(
        cls, gt: float, area_isolador_m2: float, pressao_dinamica_pa: float
    ) -> float:
        """Força (N) do vento em cadeia de isoladores (arrasto padrão)."""
        if area_isolador_m2 <= 0:
            raise ValueError("Área do isolador deve ser positiva.")
        F = gt * area_isolador_m2 * pressao_dinamica_pa * cls.COEF_ARRASTO_ISOLADOR
        return float(round(F, 2))

    @classmethod
    def forca_vento_em_cabo(
        cls,
        *,
        gl: float,
        gc: float,
        pressao_dinamica_pa: float,
        angulo_incidencia_graus: float,
        diametro_m: float,
        comprimento_vao_m: float,
        coef_arrasto: Optional[float] = None,
    ) -> float:
        """Força (N) do vento em cabo (incidência no plano do vão)."""
        if not (0.0 <= angulo_incidencia_graus <= 90.0):
            raise ValueError("Ângulo de incidência deve estar entre 0 e 90 graus.")
        if diametro_m <= 0 or comprimento_vao_m <= 0:
            raise ValueError("Diâmetro e comprimento de vão devem ser positivos.")
        if coef_arrasto is None:
            coef_arrasto = cls.coef_arrasto_cabo(diametro_m)

        seno = math.sin(math.radians(angulo_incidencia_graus))
        F = gc * gl * pressao_dinamica_pa * coef_arrasto * diametro_m * comprimento_vao_m * (seno ** 2)
        return float(round(F, 2))

    # -------------------- Mudança de estado (C++ via pybind11) --------------------
    @classmethod
    def mudar_estado_cabo(
        cls,
        modulo_elasticidade_pa: float,
        area_secao_m2: float,
        peso_unit_inicial_npm: float,
        peso_unit_final_npm: float,
        tracao_inicial_n: float,
        temp_inicial_c: float,
        temp_final_c: float,
        alfa_thermal_1porc: float,
        comprimento_vao_m: float,
    ) -> float:
        """
        Calcula a nova tração (N) chamando o módulo C++ compilado 'estado_cpp'.
        """
        try:
            # Delega o cálculo pesado para a função C++ importada
            return estado_cpp.mudar_estado_cabo(
                modulo_elasticidade_pa=modulo_elasticidade_pa,
                area_secao_m2=area_secao_m2,
                peso_unit_inicial_npm=peso_unit_inicial_npm,
                peso_unit_final_npm=peso_unit_final_npm,
                tracao_inicial_n=tracao_inicial_n,
                temp_inicial_c=temp_inicial_c,
                temp_final_c=temp_final_c,
                alfa_thermal_1porc=alfa_thermal_1porc,
                comprimento_vao_m=comprimento_vao_m,
            )
        except NameError:
            # Erro comum se o import falhar no __main__
            raise RuntimeError("Módulo 'estado_cpp' não foi importado. Compile o projeto primeiro.")
        except Exception as e:
            # Captura exceções do C++ (invalid_argument, runtime_error)
            # e as re-lança como uma exceção Python para manter a consistência.
            raise RuntimeError(f"Erro no cálculo C++: {e}") from e


# =============================================================
# Caso de carga e coleção de casos
# =============================================================

@dataclass(slots=True)
class CasoDeCarga:
    """
    Parâmetros meteorológicos/ambientais de uma condição de cálculo.
    Se altitude_m/tipo_terreno forem omitidos, herda de AmbientePadrao.
    """
    # Obrigatórios
    descricao: str
    velocidade_vento_ms: float
    periodo_retorno_anos: float
    tempo_integracao_s: float
    temperatura_condutor_c: float
    temperatura_ambiente_c: float

    # Opcionais
    angulo_incidencia_graus: float = 90.0  # 0..90 (no plano do vão)
    altitude_m: Optional[float] = None
    tipo_terreno: Optional[Union[TipoTerreno, str]] = None
    pressao_atm_pa: Optional[float] = None
    massa_especifica_ar_kgm3: Optional[float] = None
    tags: Tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        # Normaliza tipo de terreno
        if isinstance(self.tipo_terreno, str) and self.tipo_terreno:
            try:
                self.tipo_terreno = TipoTerreno[self.tipo_terreno.upper()]
            except KeyError as e:
                raise ValueError("tipo_terreno deve ser 'A', 'B', 'C' ou 'D'.") from e

        # Defaults de ambiente
        if self.altitude_m is None:
            self.altitude_m = AmbientePadrao.altitude_m
        if self.tipo_terreno is None:
            self.tipo_terreno = AmbientePadrao.tipo_terreno

        # Validações
        self._validar()

        # Derivados
        if self.pressao_atm_pa is None:
            self.pressao_atm_pa = CalculadoraNBR5422.calcular_pressao_padrao(self.altitude_m)
        if self.massa_especifica_ar_kgm3 is None:
            self.massa_especifica_ar_kgm3 = CalculadoraNBR5422.calcular_massa_especifica_ar(
                self.temperatura_ambiente_c, self.altitude_m
            )

    def _validar(self) -> None:
        if self.velocidade_vento_ms < 0:
            raise ValueError("Velocidade do vento deve ser não negativa.")
        if self.periodo_retorno_anos <= 0:
            raise ValueError("Período de retorno deve ser positivo.")
        if self.tempo_integracao_s <= 0:
            raise ValueError("Tempo de integração deve ser positivo.")
        if not (0.0 <= self.angulo_incidencia_graus <= 90.0):
            raise ValueError("Ângulo de incidência deve estar entre 0 e 90 graus.")
        if not isinstance(self.tipo_terreno, TipoTerreno):
            raise ValueError("tipo_terreno inválido.")
        if self.altitude_m is None or self.altitude_m < 0:
            raise ValueError("altitude_m deve ser não negativa.")

    # --------- propriedades derivadas ---------
    @property
    def densidade_relativa_ar(self) -> float:
        return CalculadoraNBR5422.calcular_densidade_relativa_ar(
            self.pressao_atm_pa, self.temperatura_ambiente_c
        )

    @property
    def pressao_dinamica_pa(self) -> float:
        return CalculadoraNBR5422.calcular_pressao_dinamica(
            self.massa_especifica_ar_kgm3, self.velocidade_vento_ms
        )

    # --------- utilitários para cálculo de vento ---------
    def fatores_vento(self, *, altura_cabo_m: float, comprimento_vao_m: float) -> Tuple[float, float, float]:
        gc = CalculadoraNBR5422.calcular_gc(altura_cabo_m, self.tipo_terreno)   # cabo
        gl = CalculadoraNBR5422.calcular_gl(comprimento_vao_m)                  # efetividade
        gt = CalculadoraNBR5422.calcular_gt(altura_cabo_m, self.tipo_terreno)   # suporte/isolador
        return gc, gl, gt

    def forca_vento_cabo(
        self,
        *,
        altura_cabo_m: float,
        comprimento_vao_m: float,
        diametro_cabo_m: float,
        coef_arrasto: Optional[float] = None,
    ) -> float:
        gc, gl, _ = self.fatores_vento(altura_cabo_m=altura_cabo_m, comprimento_vao_m=comprimento_vao_m)
        return CalculadoraNBR5422.forca_vento_em_cabo(
            gl=gl,
            gc=gc,
            pressao_dinamica_pa=self.pressao_dinamica_pa,
            angulo_incidencia_graus=self.angulo_incidencia_graus,
            diametro_m=diametro_cabo_m,
            comprimento_vao_m=comprimento_vao_m,
            coef_arrasto=coef_arrasto,
        )

    def forca_vento_isolador(
        self,
        *,
        altura_cabo_m: float,
        area_isolador_m2: float
    ) -> float:
        _, _, gt = self.fatores_vento(altura_cabo_m=altura_cabo_m, comprimento_vao_m=CalculadoraNBR5422.ALTURA_MINIMA_CALCULO)
        return CalculadoraNBR5422.forca_vento_em_isolador(
            gt=gt, area_isolador_m2=area_isolador_m2, pressao_dinamica_pa=self.pressao_dinamica_pa
        )

    # --------- resumo ---------
    def resumo(self) -> str:
        linhas = [
            "=== CASO DE CARGA ===",
            f"Descrição: {self.descricao}",
            f"Tags: {', '.join(self.tags) if self.tags else '-'}",
            "",
            "VENTO:",
            f"  Velocidade: {self.velocidade_vento_ms:.2f} m/s",
            f"  Ângulo incidência (0–90): {self.angulo_incidencia_graus:g}°",
            f"  Período de retorno: {self.periodo_retorno_anos:g} anos",
            f"  Tempo de integração: {self.tempo_integracao_s:g} s",
            f"  Pressão dinâmica: {self.pressao_dinamica_pa:.1f} Pa",
            "",
            "TEMPERATURAS:",
            f"  Ambiente: {self.temperatura_ambiente_c:.1f} °C",
            f"  Condutor: {self.temperatura_condutor_c:.1f} °C",
            "",
            "ATMOSFERA:",
            f"  Altitude: {self.altitude_m:.1f} m",
            f"  Pressão: {self.pressao_atm_pa:.1f} Pa",
            f"  Massa específica: {self.massa_especifica_ar_kgm3:.3f} kg/m³",
            f"  Densidade relativa: {self.densidade_relativa_ar:.3f}",
            f"  Terreno: {self.tipo_terreno.value}",
        ]
        return "\n".join(linhas)


# ------------------- Coleção iterável de casos -------------------

@dataclass
class CasosDeCarga:
    """Coleção ordenada de casos com helpers para gerar/iterar/avaliar."""
    _lista: List[CasoDeCarga] = field(default_factory=list)

    # ---- protocolo de coleção ----
    def __iter__(self) -> Iterator[CasoDeCarga]:
        return iter(self._lista)

    def __len__(self) -> int:
        return len(self._lista)

    def __getitem__(self, idx: int) -> CasoDeCarga:
        return self._lista[idx]

    # ---- construção/adição ----
    def add(self, caso: CasoDeCarga) -> "CasosDeCarga":
        self._lista.append(caso)
        return self

    def add_many(self, casos: Iterable[CasoDeCarga]) -> "CasosDeCarga":
        self._lista.extend(casos)
        return self

    @staticmethod
    def _rotulo_var(valor: Any) -> str:
        if isinstance(valor, float):
            # rótulo compacto para floats (ex.: 32.0 -> 32)
            return f"{valor:.3g}".rstrip("0").rstrip(".")
        return str(valor)

    @classmethod
    def a_partir_de_grade(
        cls,
        caso_base: CasoDeCarga,
        **grade_variaveis: Sequence[Any],
    ) -> "CasosDeCarga":
        """
        Gera combinações (cartesiano) variando campos do caso_base.
        Ex.: a_partir_de_grade(base, velocidade_vento_ms=[0,10,20], angulo_incidencia_graus=[0,90])
        """
        chaves = list(grade_variaveis.keys())
        valores = [list(v) for v in grade_variaveis.values()]
        combinacoes = itertools.product(*valores)

        casos: List[CasoDeCarga] = []
        for combo in combinacoes:
            kwargs = {k: v for k, v in zip(chaves, combo)}
            # monta descrição com sufixos auto-explicativos
            sufixos = [f"{k}={cls._rotulo_var(v)}" for k, v in kwargs.items()]
            desc = f"{caso_base.descricao} | " + ", ".join(sufixos)
            novo = CasoDeCarga(
                descricao=desc,
                velocidade_vento_ms=kwargs.get("velocidade_vento_ms", caso_base.velocidade_vento_ms),
                periodo_retorno_anos=kwargs.get("periodo_retorno_anos", caso_base.periodo_retorno_anos),
                tempo_integracao_s=kwargs.get("tempo_integracao_s", caso_base.tempo_integracao_s),
                temperatura_condutor_c=kwargs.get("temperatura_condutor_c", caso_base.temperatura_condutor_c),
                temperatura_ambiente_c=kwargs.get("temperatura_ambiente_c", caso_base.temperatura_ambiente_c),
                angulo_incidencia_graus=kwargs.get("angulo_incidencia_graus", caso_base.angulo_incidencia_graus),
                altitude_m=kwargs.get("altitude_m", caso_base.altitude_m),
                tipo_terreno=kwargs.get("tipo_terreno", caso_base.tipo_terreno),
                pressao_atm_pa=kwargs.get("pressao_atm_pa", caso_base.pressao_atm_pa),
                massa_especifica_ar_kgm3=kwargs.get("massa_especifica_ar_kgm3", caso_base.massa_especifica_ar_kgm3),
                tags=kwargs.get("tags", caso_base.tags),
            )
            casos.append(novo)
        return cls(casos)

    # ---- transformação/aplicação ----
    def map(self, func: Callable[[CasoDeCarga], Any]) -> List[Any]:
        """Aplica uma função a cada caso e retorna a lista de resultados."""
        return [func(c) for c in self._lista]

    def filtrar(self, predicado: Callable[[CasoDeCarga], bool]) -> "CasosDeCarga":
        """Retorna uma nova coleção apenas com casos que satisfazem o predicado."""
        return CasosDeCarga([c for c in self._lista if predicado(c)])

    # ---- avaliações prontas ----
    def avaliar_forcas(
        self,
        *,
        altura_cabo_m: float,
        comprimento_vao_m: float,
        diametro_cabo_m: float,
        area_isolador_m2: Optional[float] = None,
        coef_arrasto_cabo: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Calcula, para todos os casos, as forças de vento no cabo (e no isolador se área for dada).
        Retorna uma lista de dicionários (fácil de jogar para Excel/CSV/DataFrame).
        """
        tabela: List[Dict[str, Any]] = []
        for c in self._lista:
            gc, gl, gt = c.fatores_vento(altura_cabo_m=altura_cabo_m, comprimento_vao_m=comprimento_vao_m)
            F_cabo = CalculadoraNBR5422.forca_vento_em_cabo(
                gl=gl,
                gc=gc,
                pressao_dinamica_pa=c.pressao_dinamica_pa,
                angulo_incidencia_graus=c.angulo_incidencia_graus,
                diametro_m=diametro_cabo_m,
                comprimento_vao_m=comprimento_vao_m,
                coef_arrasto=coef_arrasto_cabo,
            )
            linha = {
                "descricao": c.descricao,
                "tags": ",".join(c.tags),
                "V_ms": c.velocidade_vento_ms,
                "angulo_graus": c.angulo_incidencia_graus,
                "TR_anos": c.periodo_retorno_anos,
                "Tint_s": c.tempo_integracao_s,
                "Tcond_C": c.temperatura_condutor_c,
                "Tamb_C": c.temperatura_ambiente_c,
                "alt_m": c.altitude_m,
                "terreno": c.tipo_terreno.value,
                "rho_kgm3": c.massa_especifica_ar_kgm3,
                "q_Pa": c.pressao_dinamica_pa,
                "GC": gc,
                "GL": gl,
                "GT": gt,
                "F_vento_cabo_N": F_cabo,
            }
            if area_isolador_m2 is not None and area_isolador_m2 > 0:
                F_isol = CalculadoraNBR5422.forca_vento_em_isolador(
                    gt=gt, area_isolador_m2=area_isolador_m2, pressao_dinamica_pa=c.pressao_dinamica_pa
                )
                linha["F_vento_isolador_N"] = F_isol
            tabela.append(linha)
        return tabela


# =============================================================
# Exemplo de uso
# =============================================================

if __name__ == "__main__":
    # --- Bloco de Importação do Módulo C++ ---
    import sys
    import os

    # Adiciona o diretório de build ao path para que o Python encontre o .pyd
    # Isso torna o script executável da raiz do projeto.
    build_dir = os.path.join(os.path.dirname(__file__), 'build', 'Release')
    if not os.path.isdir(build_dir):
        # Fallback para configurações de build que não criam subpasta 'Release'
        build_dir = os.path.join(os.path.dirname(__file__), 'build')

    sys.path.insert(0, build_dir)

    try:
        import estado_cpp
        print("INFO: Módulo C++ 'estado_cpp' importado com sucesso.")
    except ImportError:
        print("="*60)
        print("ERRO: Módulo C++ 'estado_cpp' não encontrado.")
        print(f"Verifique se o módulo foi compilado e existe em: {build_dir}")
        print("\nExecute os comandos de compilação antes de rodar o script:")
        print("  1. cmake -B build -A x64")
        print("  2. cmake --build build --config Release")
        print("="*60)
        sys.exit(1)
    # --- Fim do Bloco de Importação ---

    print("\n=== EXEMPLOS (usando o módulo C++ para mudança de estado) ===\n")


    # 1) Defina uma vez os padrões do projeto
    AmbientePadrao.set_defaults(altitude_m=800.0, tipo_terreno="B")

    # 2) Monte seus casos à vontade (quantos quiser)
    #    Exemplos típicos
    eds = CasoDeCarga(
        descricao="EDS",
        velocidade_vento_ms=0.0,
        periodo_retorno_anos=50.0,
        tempo_integracao_s=600.0,
        temperatura_condutor_c=25.0,
        temperatura_ambiente_c=25.0,
        angulo_incidencia_graus=0.0,
        tags=("EDS",),
    )

    vento_max = CasoDeCarga(
        descricao="Vento máximo 50a 10min",
        velocidade_vento_ms=32.0,
        periodo_retorno_anos=50.0,
        tempo_integracao_s=600.0,   # 10 min
        temperatura_condutor_c=15.0,
        temperatura_ambiente_c=15.0,
        angulo_incidencia_graus=90.0,
        tags=("VentoMax",),
    )

    casos = CasosDeCarga().add(eds).add(vento_max)

    # 3) Ou gere N casos por grade (ex.: diferentes V e ângulos a partir de um base)
    base = CasoDeCarga(
        descricao="Base verão",
        velocidade_vento_ms=10.0,
        periodo_retorno_anos=50.0,
        tempo_integracao_s=600.0,
        temperatura_condutor_c=70.0,
        temperatura_ambiente_c=35.0,
        angulo_incidencia_graus=90.0,
        tags=("operacao",),
    )
    grade = CasosDeCarga.a_partir_de_grade(
        base,
        velocidade_vento_ms=[0.0, 10.0, 20.0, 32.0],
        angulo_incidencia_graus=[0.0, 45.0, 90.0],
    )

    casos.add_many(grade)

    # 4) Parâmetros geométricos para avaliação única (poderia variar por-caso se quiser)
    altura_cabo_m = 25.0
    vao_m = 400.0
    diametro_m = 0.032
    area_isolador_m2 = 0.20

    # 5) Avaliação em lote
    tabela = casos.avaliar_forcas(
        altura_cabo_m=altura_cabo_m,
        comprimento_vao_m=vao_m,
        diametro_cabo_m=diametro_m,
        area_isolador_m2=area_isolador_m2,
        # coef_arrasto_cabo=None  # deixe None para usar regra automática (1.2 se d<15mm; senão 1.0)
    )

    # 6) Exemplo de saída compacta
    print(f"Foram avaliados {len(tabela)} casos.\n")
    for linha in tabela[:5]:  # mostra só os 5 primeiros
        print(
            f"- {linha['descricao']}: V={linha['V_ms']} m/s, ângulo={linha['angulo_graus']}°, "
            f"q={linha['q_Pa']} Pa, GC={linha['GC']}, GL={linha['GL']:.3f}, "
            f"F_cabo={linha['F_vento_cabo_N']:.1f} N"
            + (f", F_isol={linha['F_vento_isolador_N']:.1f} N" if 'F_vento_isolador_N' in linha else "")
        )

    # 7) Se quiser, o resumo de um caso específico
    print("\nResumo do caso 'Vento máximo 50a 10min':\n")
    print(vento_max.resumo())

      # ----------------------------------------------------------------------
    # 8) Exemplo: Mudança de estado do cabo (EDS -> Vento máximo)
    # ----------------------------------------------------------------------
    # Hipóteses (ajuste para o seu condutor real):
    E_pa = 70e9                  # Módulo equivalente do cabo (Pa) ~ 70 GPa
    area_m2 = 3.0e-4             # Área efetiva (m²) ~ 300 mm²
    w_self_npm = 13.0            # Peso próprio do condutor (N/m) ~ 1,3 kg/m
    T_inicial_N = 20_000.0       # Tração inicial (N) no estado EDS
    alpha_1porC = 19e-6          # Coef. dilatação térmica equivalente (1/°C)

    # Estado inicial: EDS (sem vento, temperatura mais alta)
    temp_ini_C = eds.temperatura_condutor_c     # 25°C
    w_ini_npm = w_self_npm                      # sem ação de vento na EDS

    # Estado final: vento máximo (usa pressão dinâmica do "vento_max")
    temp_fin_C = vento_max.temperatura_condutor_c  # 15°C
    q_Pa = vento_max.pressao_dinamica_pa
    Cd = CalculadoraNBR5422.coef_arrasto_cabo(diametro_m)
    w_vento_npm = q_Pa * Cd * diametro_m             # força horizontal por metro (N/m)

    # Peso resultante por metro (combinação vetorial de próprio + vento)
    w_fin_npm = math.hypot(w_self_npm, w_vento_npm)

    # Calcula a nova tração pela sua rotina iterativa
    t0 = time.perf_counter()
    try:
        T_final_N = CalculadoraNBR5422.mudar_estado_cabo(
            modulo_elasticidade_pa=E_pa,
            area_secao_m2=area_m2,
            peso_unit_inicial_npm=w_ini_npm,
            peso_unit_final_npm=w_fin_npm,
            tracao_inicial_n=T_inicial_N,
            temp_inicial_c=temp_ini_C,
            temp_final_c=temp_fin_C,
            alfa_thermal_1porc=alpha_1porC,
            comprimento_vao_m=vao_m,
        )
    except RuntimeError as e:
        T_final_N = float('nan')
        print(f"[Mudança de estado] Não convergiu: {e}")

    dt = time.perf_counter() - t0
    print(f"Tempo para mudança de estado: {dt*1000:.2f} ms")
    
    # Flecha aproximada (parabólica) para comparação rápida
    def flecha_parabolica(w_npm: float, L_m: float, T_N: float) -> float:
        return (w_npm * (L_m ** 2)) / (8.0 * T_N)

    f_ini_m = flecha_parabolica(w_ini_npm, vao_m, T_inicial_N)
    f_fin_m = flecha_parabolica(w_fin_npm, vao_m, T_final_N) if T_final_N > 0 else float('nan')

    print("\n[MUDANÇA DE ESTADO: EDS → Vento máx]")
    print(f"  q (vento máx)            : {q_Pa:,.1f} Pa")
    print(f"  Cd (automático)          : {Cd:.2f}")
    print(f"  w_self (N/m)             : {w_self_npm:.2f}")
    print(f"  w_vento (N/m)            : {w_vento_npm:.2f}")
    print(f"  w_final (resultante N/m) : {w_fin_npm:.2f}")
    print(f"  T_inicial (EDS)          : {T_inicial_N:,.1f} N @ {temp_ini_C:.1f} °C")
    print(f"  T_final  (Vento máx)     : {T_final_N:,.1f} N @ {temp_fin_C:.1f} °C")
    print(f"  Flecha inicial (aprox)   : {f_ini_m:.3f} m")
    print(f"  Flecha final (aprox)     : {f_fin_m:.3f} m")
