#include <iostream>
#include <vector>
#include <omp.h>
#include <cmath>

using namespace std;

struct Particula { int id; double x, y; };

struct QuadNo {
    double x0, x1, y0, y1;
    bool folha = true;
    vector<Particula> pts;
    QuadNo *nw=0, *ne=0, *sw=0, *se=0;
    
    QuadNo(double x0, double x1, double y0, double y1) : x0(x0), x1(x1), y0(y0), y1(y1) {}
};

// --- CONSTRUÇÃO PARALELA (TASKS) ---
void construir_arvore(QuadNo* no, const vector<Particula>& pts, int prof) {
    // Parada: Max 50 por nó ou se aprofundou demais (pra não dar stack overflow)
    if (pts.size() <= 50 || prof >= 20) {
        no->pts = pts;
        return;
    }

    no->folha = false;
    double mx = (no->x0 + no->x1) / 2.0;
    double my = (no->y0 + no->y1) / 2.0;

    no->nw = new QuadNo(no->x0, mx, my, no->y1);
    no->ne = new QuadNo(mx, no->x1, my, no->y1);
    no->sw = new QuadNo(no->x0, mx, no->y0, my);
    no->se = new QuadNo(mx, no->x1, no->y0, my);

    vector<Particula> p_nw, p_ne, p_sw, p_se;
    for (auto& p : pts) {
        if (p.x <= mx && p.y >= my) p_nw.push_back(p);
        else if (p.x > mx && p.y >= my) p_ne.push_back(p);
        else if (p.x <= mx && p.y < my) p_sw.push_back(p);
        else p_se.push_back(p);
    }

    // Cutoff (limite de profundidade para as tasks)
    if (prof < 5) {
        #pragma omp task shared(no)
        construir_arvore(no->nw, p_nw, prof + 1);
        #pragma omp task shared(no)
        construir_arvore(no->ne, p_ne, prof + 1);
        #pragma omp task shared(no)
        construir_arvore(no->sw, p_sw, prof + 1);
        #pragma omp task shared(no)
        construir_arvore(no->se, p_se, prof + 1);
        #pragma omp taskwait
    } else {
        // Passou do cutoff, faz sequencial pra não gerar overhead no OpenMP
        construir_arvore(no->nw, p_nw, prof + 1);
        construir_arvore(no->ne, p_ne, prof + 1);
        construir_arvore(no->sw, p_sw, prof + 1);
        construir_arvore(no->se, p_se, prof + 1);
    }
}

// Verifica se a área de busca cruza o quadrante atual
void buscar_vizinhos(QuadNo* no, double px, double py, double r, vector<int>& vizinhos) {
    double cx = max(no->x0, min(px, no->x1));
    double cy = max(no->y0, min(py, no->y1));
    
    // Fora do raio
    if ((px - cx)*(px - cx) + (py - cy)*(py - cy) > r*r) return;

    if (no->folha) {
        for (auto& p : no->pts) {
            if ((p.x - px)*(p.x - px) + (p.y - py)*(p.y - py) <= r*r) {
                vizinhos.push_back(p.id);
            }
        }
        return;
    }

    buscar_vizinhos(no->nw, px, py, r, vizinhos);
    buscar_vizinhos(no->ne, px, py, r, vizinhos);
    buscar_vizinhos(no->sw, px, py, r, vizinhos);
    buscar_vizinhos(no->se, px, py, r, vizinhos);
}

int main() {
    int N = 100000;
    double R = 10.0;
    vector<Particula> pts(N);

    // Gera 100.000 pontos aleatórios entre 0.0 e 1000.0
    for (int i = 0; i < N; i++) {
        pts[i] = {i, (rand() % 10000) / 10.0, (rand() % 10000) / 10.0};
    }

    QuadNo* raiz = new QuadNo(0.0, 1000.0, 0.0, 1000.0);

    double t0 = omp_get_wtime();
    // Pra criar tasks soltas, precisa abrir a região paralela antes e usar o single
    #pragma omp parallel
    {
        #pragma omp single
        construir_arvore(raiz, pts, 0);
    }
    cout << "Tempo construcao (tasks): " << omp_get_wtime() - t0 << " s\n";

    vector<int> vizinhos_count(N, 0);
    
    t0 = omp_get_wtime();
    
    // --- CONSULTA PARALELA (READ-ONLY) ---
    #pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < N; i++) {
        vector<int> vizinhos;
        buscar_vizinhos(raiz, pts[i].x, pts[i].y, R, vizinhos);
        // Tira 1 pq ele acha a própria partícula na busca
        vizinhos_count[i] = vizinhos.empty() ? 0 : vizinhos.size() - 1; 
    }
    cout << "Tempo consulta (todas as 100k): " << omp_get_wtime() - t0 << " s\n";

    return 0;
}