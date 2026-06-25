#include <iostream>
#include <vector>
#include <omp.h>
#include <cmath>

using namespace std;

struct Particula {
    int id;
    double x;
    double y;
};

struct QuadNo {
    double x0, x1, y0, y1;
    bool folha;
    vector<Particula> pts;
    QuadNo *nw, *ne, *sw, *se;

    // Construtor mais padronizado
    QuadNo(double x0, double x1, double y0, double y1) {
        this->x0 = x0;
        this->x1 = x1;
        this->y0 = y0;
        this->y1 = y1;
        this->folha = true; // começa como folha por padrão
        this->nw = nullptr;
        this->ne = nullptr;
        this->sw = nullptr;
        this->se = nullptr;
    }
};

// --- CONSTRUÇÃO PARALELA (TASKS) ---
void construir_arvore(QuadNo* no, const vector<Particula>& pts, int nivel) {
    // Condição de parada: Max 50 pontos ou aprofundou demais (pra evitar stack overflow)
    if (pts.size() <= 50 || nivel >= 20) {
        no->pts = pts;
        return;
    }

    no->folha = false;
    
    // Pega o meio do quadrante atual
    double meio_x = (no->x0 + no->x1) / 2.0;
    double meio_y = (no->y0 + no->y1) / 2.0;

    no->nw = new QuadNo(no->x0, meio_x, meio_y, no->y1);
    no->ne = new QuadNo(meio_x, no->x1, meio_y, no->y1);
    no->sw = new QuadNo(no->x0, meio_x, no->y0, meio_y);
    no->se = new QuadNo(meio_x, no->x1, no->y0, meio_y);

    // Separando as particulas em cada quadrante usando loop normal
    vector<Particula> p_nw, p_ne, p_sw, p_se;
    for (int i = 0; i < pts.size(); i++) {
        Particula p = pts[i];
        if (p.x <= meio_x && p.y >= meio_y) {
            p_nw.push_back(p);
        } else if (p.x > meio_x && p.y >= meio_y) {
            p_ne.push_back(p);
        } else if (p.x <= meio_x && p.y < meio_y) {
            p_sw.push_back(p);
        } else {
            p_se.push_back(p);
        }
    }

    // Cutoff do OpenMP: limita a criação de tasks pra não pesar muito
    if (nivel < 5) {
        #pragma omp task shared(no)
        construir_arvore(no->nw, p_nw, nivel + 1);

        #pragma omp task shared(no)
        construir_arvore(no->ne, p_ne, nivel + 1);

        #pragma omp task shared(no)
        construir_arvore(no->sw, p_sw, nivel + 1);

        #pragma omp task shared(no)
        construir_arvore(no->se, p_se, nivel + 1);

        // Espera as tasks acabarem senão os vetores perdem a referencia
        #pragma omp taskwait
    } else {
        // Se passou do limite (cutoff), vai sequencial mesmo
        construir_arvore(no->nw, p_nw, nivel + 1);
        construir_arvore(no->ne, p_ne, nivel + 1);
        construir_arvore(no->sw, p_sw, nivel + 1);
        construir_arvore(no->se, p_se, nivel + 1);
    }
}

// Verifica se a área de busca cruza o quadrante atual
void buscar_vizinhos(QuadNo* no, double px, double py, double r, vector<int>& vizinhos) {
    // Acha o ponto mais proximo dentro do quadrado pra checar a colisao
    double cx = px;
    if (px < no->x0) cx = no->x0;
    else if (px > no->x1) cx = no->x1;

    double cy = py;
    if (py < no->y0) cy = no->y0;
    else if (py > no->y1) cy = no->y1;

    // Calcula a distancia
    double dist2 = (px - cx)*(px - cx) + (py - cy)*(py - cy);
    
    // Se tiver totalmente fora do raio de busca, ignora e volta
    if (dist2 > r*r) {
        return;
    }

    // Se achou uma folha, confere as particulas uma por uma
    if (no->folha) {
        for (int i = 0; i < no->pts.size(); i++) {
            Particula p = no->pts[i];
            double d2 = (p.x - px)*(p.x - px) + (p.y - py)*(p.y - py);
            if (d2 <= r*r) {
                vizinhos.push_back(p.id);
            }
        }
        return;
    }

    // Se nao for folha, continua descendo na arvore
    buscar_vizinhos(no->nw, px, py, r, vizinhos);
    buscar_vizinhos(no->ne, px, py, r, vizinhos);
    buscar_vizinhos(no->sw, px, py, r, vizinhos);
    buscar_vizinhos(no->se, px, py, r, vizinhos);
}

int main() {
    int N = 100000;
    double R = 10.0;
    vector<Particula> pts(N);

    // Gerando os 100.000 pontos aleatorios
    for (int i = 0; i < N; i++) {
        pts[i].id = i;
        pts[i].x = (rand() % 10000) / 10.0;
        pts[i].y = (rand() % 10000) / 10.0;
    }

    QuadNo* raiz = new QuadNo(0.0, 1000.0, 0.0, 1000.0);

    double tempo_inicio = omp_get_wtime();
    
    // Abre a regiao paralela e usa o single pro mestre iniciar as tasks
    #pragma omp parallel
    {
        #pragma omp single
        construir_arvore(raiz, pts, 0);
    }
    
    cout << "Tempo construcao (com tasks): " << omp_get_wtime() - tempo_inicio << " s\n";

    vector<int> vizinhos_count(N, 0);
    tempo_inicio = omp_get_wtime();
    
    // --- CONSULTA PARALELA (READ-ONLY) ---
    // Usando schedule dynamic pra balancear a carga das threads
    #pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < N; i++) {
        vector<int> vizinhos;
        buscar_vizinhos(raiz, pts[i].x, pts[i].y, R, vizinhos);
        
        // Desconta 1 porque o codigo acha a propria particula dentro do raio
        if (vizinhos.size() > 0) {
            vizinhos_count[i] = vizinhos.size() - 1;
        } else {
            vizinhos_count[i] = 0;
        }
    }
    
    cout << "Tempo consulta (100k pontos): " << omp_get_wtime() - tempo_inicio << " s\n";

    return 0;
}