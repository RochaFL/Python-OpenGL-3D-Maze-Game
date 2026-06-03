import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

# =============================================================================
# DEFINIÇÃO DO MAPA DO LABIRINTO
# 'P' = Parede, 'C' = Cristal/Coletável, ' ' = Espaço Vazio
# =============================================================================
MAPA = [
    "PPPPPPPPPPPP",
    "P C        P",
    "P P P PP P P",
    "P P C PP P P",
    "P P   P  C P",
    "P PPP P PP P",
    "P C P   P  P",
    "P P PPP PP P",
    "P   C      P",
    "PPPPPPPPPPPP",
]

TAMANHO_BLOCO = 2.0
ALTURA_PAREDE = 2.0

# =============================================================================
# FUNÇÃO PARA CARREGAR TEXTURAS
# =============================================================================

def load_texture(path):
    """Carrega uma imagem e a converte em uma textura OpenGL."""
    try:
        image = pygame.image.load(path)
        if image.get_alpha():
            image_data = pygame.image.tostring(image, "RGBA", True)
            mode = GL_RGBA
        else:
            image_data = pygame.image.tostring(image, "RGB", True)
            mode = GL_RGB
        
        width, height = image.get_width(), image.get_height()
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        glTexImage2D(GL_TEXTURE_2D, 0, mode, width, height, 0, mode, GL_UNSIGNED_BYTE, image_data)
        
        return texture_id
    except pygame.error as e:
        print(f"Erro ao carregar textura {path}: {e}")
        return None

# =============================================================================
# FUNÇÕES DE DESENHO E UI
# =============================================================================

def desenha_plano_texturizado(pos_y, largura, profundidade, repeticoes_textura, texture_id):
    """Desenha um plano horizontal (chão) com uma textura que se repete."""
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glColor3f(1.0, 1.0, 1.0)

    # Coordenadas dos 4 cantos do plano
    v1 = [0, pos_y, 0]
    v2 = [largura, pos_y, 0]
    v3 = [largura, pos_y, profundidade]
    v4 = [0, pos_y, profundidade]
    
    glBegin(GL_QUADS)
    # A repetição da textura é controlada aqui, usando 'repeticoes_textura'
    glTexCoord2f(0.0, 0.0); glVertex3fv(v1)
    glTexCoord2f(repeticoes_textura, 0.0); glVertex3fv(v2)
    glTexCoord2f(repeticoes_textura, repeticoes_textura); glVertex3fv(v3)
    glTexCoord2f(0.0, repeticoes_textura); glVertex3fv(v4)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def desenha_cubo(pos, tamanho, cor=None, texture_id=None):
    """Desenha um cubo sólido com ou sem textura."""
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])

    if texture_id:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glColor3f(1.0, 1.0, 1.0)
    elif cor:
        glColor3fv(cor)
    else:
        glColor3f(1.0, 1.0, 1.0) 
        
    half_size = tamanho / 2
    
    vertices_com_uv = [
        ([-half_size, -half_size,  half_size], (0, 0)), ([ half_size, -half_size,  half_size], (1, 0)),
        ([ half_size,  half_size,  half_size], (1, 1)), ([-half_size,  half_size,  half_size], (0, 1)),
        ([-half_size, -half_size, -half_size], (1, 0)), ([ half_size, -half_size, -half_size], (0, 0)),
        ([ half_size,  half_size, -half_size], (0, 1)), ([-half_size,  half_size, -half_size], (1, 1)),
        ([-half_size,  half_size,  half_size], (0, 0)), ([ half_size,  half_size,  half_size], (1, 0)),
        ([ half_size,  half_size, -half_size], (1, 1)), ([-half_size,  half_size, -half_size], (0, 1)),
        ([-half_size, -half_size,  half_size], (0, 1)), ([ half_size, -half_size,  half_size], (1, 1)),
        ([ half_size, -half_size, -half_size], (1, 0)), ([-half_size, -half_size, -half_size], (0, 0)),
        ([ half_size, -half_size,  half_size], (0, 0)), ([ half_size, -half_size, -half_size], (1, 0)),
        ([ half_size,  half_size, -half_size], (1, 1)), ([ half_size,  half_size,  half_size], (0, 1)),
        ([-half_size, -half_size, -half_size], (0, 0)), ([-half_size, -half_size,  half_size], (1, 0)),
        ([-half_size,  half_size,  half_size], (1, 1)), ([-half_size,  half_size, -half_size], (0, 1))
    ]
    
    faces_indices = [
        (0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11),
        (12, 13, 14, 15), (16, 17, 18, 19), (20, 21, 22, 23)
    ]

    glBegin(GL_QUADS)
    for face in faces_indices:
        for vert_idx in face:
            glTexCoord2fv(vertices_com_uv[vert_idx][1])
            glVertex3fv(vertices_com_uv[vert_idx][0])
    glEnd()

    if texture_id:
        glDisable(GL_TEXTURE_2D)
    glPopMatrix()


def desenha_piramide(pos, tamanho, cor=None, angulo=0, texture_id=None):
    """Desenha uma pirâmide que gira, com ou sem textura."""
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    glRotatef(angulo, 0, 1, 0)

    if texture_id:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glColor3f(1.0, 1.0, 1.0)
    elif cor:
        glColor3fv(cor)
    else:
        glColor3f(1.0, 1.0, 1.0)
        
    half_size = tamanho / 2
    top_v = [0, half_size, 0]
    base_v1 = [-half_size, -half_size, -half_size]; base_v2 = [ half_size, -half_size, -half_size]
    base_v3 = [ half_size, -half_size,  half_size]; base_v4 = [-half_size, -half_size,  half_size]

    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.5, 1.0); glVertex3fv(top_v); glTexCoord2f(0.0, 0.0); glVertex3fv(base_v1); glTexCoord2f(1.0, 0.0); glVertex3fv(base_v2)
    glTexCoord2f(0.5, 1.0); glVertex3fv(top_v); glTexCoord2f(0.0, 0.0); glVertex3fv(base_v2); glTexCoord2f(1.0, 0.0); glVertex3fv(base_v3)
    glTexCoord2f(0.5, 1.0); glVertex3fv(top_v); glTexCoord2f(0.0, 0.0); glVertex3fv(base_v3); glTexCoord2f(1.0, 0.0); glVertex3fv(base_v4)
    glTexCoord2f(0.5, 1.0); glVertex3fv(top_v); glTexCoord2f(0.0, 0.0); glVertex3fv(base_v4); glTexCoord2f(1.0, 0.0); glVertex3fv(base_v1)
    glEnd()

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0); glVertex3fv(base_v4); glTexCoord2f(1.0, 1.0); glVertex3fv(base_v3)
    glTexCoord2f(1.0, 0.0); glVertex3fv(base_v2); glTexCoord2f(0.0, 0.0); glVertex3fv(base_v1)
    glEnd()
    
    if texture_id:
        glDisable(GL_TEXTURE_2D)
    glPopMatrix()


def draw_text(x, y, text, font, color=(255, 255, 255, 255), bgcolor=(0, 0, 0, 128)):
    """Desenha texto 2D na tela."""
    text_surface = font.render(text, True, color, bgcolor)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glPushAttrib(GL_ALL_ATTRIB_BITS) 
    glWindowPos2d(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glPopAttrib()

def setup_2d_projection(display):
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity()
    gluOrtho2D(0, display[0], 0, display[1])
    glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
    glDisable(GL_DEPTH_TEST)

def restore_3d_projection():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION); glPopMatrix()
    glMatrixMode(GL_MODELVIEW); glPopMatrix()


class Camera:
    def __init__(self, pos_inicial):
        self.posicao = np.array(pos_inicial, dtype=float)
        self.frente = np.array([0.0, 0.0, -1.0])
        self.cima = np.array([0.0, 1.0, 0.0])
        self.velocidade = 0.1
        self.sensibilidade_mouse = 0.1
        self.yaw = -90.0
        self.pitch = 0.0
        self.raio_colisao = 0.4 

    def atualiza_vetores_camera(self):
        frente_x = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        frente_y = math.sin(math.radians(self.pitch))
        frente_z = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        self.frente = np.array([frente_x, frente_y, frente_z])
        self.frente /= np.linalg.norm(self.frente)

    def processa_mouse(self, movimento_relativo):
        dx, dy = movimento_relativo
        self.yaw += dx * self.sensibilidade_mouse
        self.pitch -= dy * self.sensibilidade_mouse
        if self.pitch > 89.0: self.pitch = 89.0
        if self.pitch < -89.0: self.pitch = -89.0
        self.atualiza_vetores_camera()
        
    def get_movimento(self, teclas):
        vetor_movimento = np.array([0.0, 0.0, 0.0])
        frente_plana = np.array([self.frente[0], 0, self.frente[2]])
        frente_plana /= np.linalg.norm(frente_plana)
        if teclas[K_w]: vetor_movimento += frente_plana * self.velocidade
        if teclas[K_s]: vetor_movimento -= frente_plana * self.velocidade
        direita = np.cross(frente_plana, self.cima)
        direita /= np.linalg.norm(direita)
        if teclas[K_a]: vetor_movimento -= direita * self.velocidade
        if teclas[K_d]: vetor_movimento += direita * self.velocidade
        return vetor_movimento

    def aplica_transformacao(self):
        ponto_olhar = self.posicao + self.frente
        gluLookAt(self.posicao[0], self.posicao[1], self.posicao[2],
                  ponto_olhar[0], ponto_olhar[1], ponto_olhar[2],
                  self.cima[0], self.cima[1], self.cima[2])

def check_collision(pos_jogador, raio_jogador, pos_caixa, tamanho_caixa):
    x_prox = max(pos_caixa[0] - tamanho_caixa / 2, min(pos_jogador[0], pos_caixa[0] + tamanho_caixa / 2))
    y_prox = max(pos_caixa[1] - tamanho_caixa / 2, min(pos_jogador[1], pos_caixa[1] + tamanho_caixa / 2))
    z_prox = max(pos_caixa[2] - tamanho_caixa / 2, min(pos_jogador[2], pos_caixa[2] + tamanho_caixa / 2))
    distancia = math.sqrt((x_prox - pos_jogador[0])**2 + (y_prox - pos_jogador[1])**2 + (z_prox - pos_jogador[2])**2)
    return distancia < raio_jogador


def main():
    pygame.init()
    display = (1024, 768)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Coletor de Cristais 3D - Final")
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    ui_font = pygame.font.Font(None, 40)
    vitoria_font = pygame.font.Font(None, 100)
    
    # Define a cor de fundo para um azul claro (céu)
    glClearColor(0.5, 0.7, 1.0, 1.0)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Carregamento de Texturas
    texture_chao = load_texture("textures/chao_grama.jpg")
    texture_parede = load_texture("textures/parede_tijolo.jpg")
    texture_cristal = load_texture("textures/cristl.png")
    if not all([texture_chao, texture_parede, texture_cristal]):
        print("Erro: Texturas não carregadas. Verifique a pasta 'textures' e os nomes dos arquivos.")
        pygame.quit(); return

    # Processa o mapa para criar listas de objetos
    paredes, coletaveis = [], []
    pos_inicial_jogador = [TAMANHO_BLOCO * 1.5, ALTURA_PAREDE / 2 + 0.5, TAMANHO_BLOCO * 1.5]
    for z, linha in enumerate(MAPA):
        for x, char in enumerate(linha):
            pos_x = x * TAMANHO_BLOCO + TAMANHO_BLOCO / 2
            pos_z = z * TAMANHO_BLOCO + TAMANHO_BLOCO / 2
            pos_y = ALTURA_PAREDE / 2
            if char == 'P':
                paredes.append({'pos': [pos_x, pos_y, pos_z], 'tamanho': TAMANHO_BLOCO})
            elif char == 'C':
                coletaveis.append({'pos': [pos_x, pos_y, pos_z], 'tamanho': 1.0, 'coletado': False, 'angulo': 0})
    
    camera = Camera(pos_inicial_jogador)
    total_coletaveis = len(coletaveis)
    coletados_count = 0
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit(); return
            if not game_over and event.type == pygame.MOUSEMOTION:
                camera.processa_mouse(event.rel)

        if not game_over:
            teclas = pygame.key.get_pressed()
            movimento = camera.get_movimento(teclas)
            proxima_pos = camera.posicao + movimento
            colidiu_com_parede = False
            for parede in paredes:
                if check_collision(proxima_pos, camera.raio_colisao, parede['pos'], parede['tamanho']):
                    colidiu_com_parede = True
                    break
            if not colidiu_com_parede:
                camera.posicao = proxima_pos
                
            for item in coletaveis:
                if not item['coletado'] and check_collision(camera.posicao, camera.raio_colisao, item['pos'], item['tamanho']):
                    item['coletado'] = True
                    coletados_count += 1
                    if coletados_count == total_coletaveis:
                        game_over = True
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluPerspective(45, (display[0] / display[1]), 0.1, 200.0)
        camera.aplica_transformacao()

        # Desenha o chão usando o novo plano texturizado
        map_width = len(MAPA[0]) * TAMANHO_BLOCO
        map_depth = len(MAPA) * TAMANHO_BLOCO
        desenha_plano_texturizado(pos_y=0, largura=map_width, profundidade=map_depth, 
                                  repeticoes_textura=map_width / 2, texture_id=texture_chao)

        # Desenha as paredes
        for parede in paredes:
            desenha_cubo(parede['pos'], parede['tamanho'], texture_id=texture_parede)
            
        # Desenha os coletáveis
        for item in coletaveis:
            if not item['coletado']:
                item['angulo'] = (item['angulo'] + 2) % 360
                desenha_piramide(item['pos'], item['tamanho'], texture_id=texture_cristal, angulo=item['angulo'])

        # Renderização da UI 2D
        setup_2d_projection(display)
        draw_text(10, display[1] - 40, f"Coletados: {coletados_count} / {total_coletaveis}", ui_font)
        if not game_over:
            tempo_decorrido = (pygame.time.get_ticks() - start_time) / 1000
            minutos = int(tempo_decorrido // 60)
            segundos = int(tempo_decorrido % 60)
            draw_text(display[0] - 190, display[1] - 40, f"Tempo: {minutos:02d}:{segundos:02d}", ui_font)
        if game_over:
            texto_vitoria = "Voce Venceu!"
            text_surf = vitoria_font.render(texto_vitoria, True, (255, 215, 0))
            pos_x = (display[0] - text_surf.get_width()) // 2
            pos_y = (display[1] - text_surf.get_height()) // 2
            draw_text(pos_x, pos_y, texto_vitoria, vitoria_font, color=(255, 215, 0), bgcolor=(0,0,0,180))
            draw_text(pos_x, pos_y - 60, "Pressione ESC para sair", ui_font, color=(255, 255, 255), bgcolor=(0,0,0,180))
        restore_3d_projection()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()