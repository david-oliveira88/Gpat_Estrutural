// mudar_estado.cpp
// Lógica de cálculo mantida, adaptada para pybind11.

#include <cmath>
#include <stdexcept>
#include <string>
#include <pybind11/pybind11.h>

namespace py = pybind11;

// A função de cálculo original, agora interna ao C++
int calcular_mudar_estado(
    double E_pa, double area_m2, double w_ini_npm, double w_fin_npm,
    double T_inicial_N, double temp_inicial_C, double temp_final_C,
    double alfa_1porC, double comprimento_vao_m, double delta_derivada,
    double precisao, int max_iter, double* T_final_out, int* iters_out)
{
    if (!T_final_out || !iters_out) return 1;
    if (E_pa <= 0.0 || area_m2 <= 0.0 || w_ini_npm <= 0.0 || w_fin_npm <= 0.0 ||
        T_inicial_N <= 0.0 || comprimento_vao_m <= 0.0 || max_iter <= 0 ||
        alfa_1porC == 0.0 || delta_derivada <= 0.0 || precisao <= 0.0) {
        return 1;
    }

    const double L = comprimento_vao_m;
    const double deltaT = temp_final_C - temp_inicial_C;
    const double tiny = 1e-12;
    const double den = (T_inicial_N / w_ini_npm) * std::sinh(w_ini_npm * L / (2.0 * T_inicial_N));

    if (std::abs(den) < tiny) return 1;

    double T = T_inicial_N;
    for (int k = 0; k < max_iter; ++k) {
        *iters_out = k + 1;

        const double num = (T / w_fin_npm) * std::sinh(w_fin_npm * L / (2.0 * T));
        const double f = (1.0 / alfa_1porC) * (num / den - 1.0) - (T - T_inicial_N) / (E_pa * area_m2) - deltaT;

        const double T_d = T + delta_derivada;
        if (T_d <= 0.0) return 1;

        const double num_d = (T_d / w_fin_npm) * std::sinh(w_fin_npm * L / (2.0 * T_d));
        const double f_d = (1.0 / alfa_1porC) * (num_d / den - 1.0) - (T_d - T_inicial_N) / (E_pa * area_m2) - deltaT;

        const double deriv = (f_d - f) / delta_derivada;
        if (std::abs(deriv) < tiny) return 2;

        double T_new = T - f / deriv;
        if (T_new <= 0.0) T_new = 0.5 * T;

        if (std::abs(f) < precisao) {
            *T_final_out = std::round(T_new * 10.0) / 10.0;
            return 0;
        }
        T = T_new;
    }
    return 3;
}

// Wrapper para pybind11 que será exposto ao Python
double mudar_estado_cabo_py(
    double E_pa, double area_m2, double w_ini_npm, double w_fin_npm,
    double T_inicial_N, double temp_inicial_C, double temp_final_C,
    double alfa_1porC, double comprimento_vao_m)
{
    // Parâmetros do solver (fixos aqui para simplicidade, iguais aos do Python)
    const double delta_derivada = 1.0;
    const double precisao = 1e-4;
    const int max_iter = 10000;

    double T_final;
    int iters;

    int ret_code = calcular_mudar_estado(
        E_pa, area_m2, w_ini_npm, w_fin_npm, T_inicial_N,
        temp_inicial_C, temp_final_C, alfa_1porC, comprimento_vao_m,
        delta_derivada, precisao, max_iter, &T_final, &iters);

    // Converte códigos de erro em exceções do Python
    switch (ret_code) {
        case 0:
            return T_final;
        case 1:
            throw std::invalid_argument("Argumentos inválidos fornecidos para mudar_estado_cabo.");
        case 2:
            throw std::runtime_error("Mudança de estado: derivada nula encontrada, sem convergência.");
        case 3:
            throw std::runtime_error("Mudança de estado: sem convergência nas iterações máximas.");
        default:
            throw std::runtime_error("Mudança de estado: erro desconhecido.");
    }
}


// Definição do módulo Python "estado_cpp"
PYBIND11_MODULE(estado_cpp, m) {
    m.doc() = "Módulo C++ para cálculo de mudança de estado de cabos (NBR 5422)";

    m.def("mudar_estado_cabo", &mudar_estado_cabo_py,
          "Calcula a nova tração em um cabo sob novas condições.",
          py::arg("modulo_elasticidade_pa"),
          py::arg("area_secao_m2"),
          py::arg("peso_unit_inicial_npm"),
          py::arg("peso_unit_final_npm"),
          py::arg("tracao_inicial_n"),
          py::arg("temp_inicial_c"),
          py::arg("temp_final_c"),
          py::arg("alfa_thermal_1porc"),
          py::arg("comprimento_vao_m")
    );
}