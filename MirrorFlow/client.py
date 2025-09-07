import socket
import struct
import threading
import pygame
import numpy as np
import zlib
import time

class LowLatencyVideoClient:
    def __init__(self, host, port=9999):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        self.frame_count = 0
        self.start_time = time.time()
        
        # Инициализация pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        pygame.display.set_caption("MirrorFlow Client")
        self.clock = pygame.time.Clock()
    
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Отключаем Nagle
            self.socket.connect((self.host, self.port))
            self.running = True
            print(f"✅ Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def receive_video(self):
        """Прием и отображение видео с минимальной задержкой"""
        buffer = b''
        expected_size = 0
        
        while self.running:
            try:
                # Получаем данные
                data = self.socket.recv(4096 * 4)
                if not data:
                    break
                
                buffer += data
                
                # Обрабатываем все complete frames в буфере
                while len(buffer) >= 4:
                    if expected_size == 0:
                        # Читаем размер frame
                        expected_size = struct.unpack('!I', buffer[:4])[0]
                        buffer = buffer[4:]
                    
                    if len(buffer) >= expected_size:
                        # Получаем frame data
                        frame_data = buffer[:expected_size]
                        buffer = buffer[expected_size:]
                        expected_size = 0
                        
                        # Декомпрессия и декодирование
                        try:
                            # Декомпрессия
                            decompressed = zlib.decompress(frame_data)
                            
                            # Конвертация в numpy array
                            nparr = np.frombuffer(decompressed, dtype=np.uint8)
                            
                            # Декодирование JPEG (если нужно) или использование raw RGB
                            # Для raw RGB предполагаем формат (height, width, 3)
                            # Нужно знать разрешение от сервера
                            frame = nparr.reshape((720, 1280, 3))  # Измените под ваше разрешение
                            
                            # Конвертация в pygame surface
                            pygame_surface = pygame.surfarray.make_surface(frame)
                            
                            # Масштабирование под размер окна
                            window_size = self.screen.get_size()
                            scaled_surface = pygame.transform.scale(pygame_surface, window_size)
                            
                            # Отображение
                            self.screen.blit(scaled_surface, (0, 0))
                            pygame.display.flip()
                            
                            # FPS counter
                            self.frame_count += 1
                            if time.time() - self.start_time >= 1.0:
                                fps = self.frame_count / (time.time() - self.start_time)
                                pygame.display.set_caption(f"MirrorFlow Client - FPS: {fps:.1f}")
                                self.frame_count = 0
                                self.start_time = time.time()
                                
                        except Exception as e:
                            print(f"Frame processing error: {e}")
                            continue
                
                # Обработка событий pygame
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                
                self.clock.tick(144)  # Высокий FPS limit
                
            except Exception as e:
                print(f"Receive error: {e}")
                break
    
    def disconnect(self):
        self.running = False
        if self.socket:
            self.socket.close()
        pygame.quit()
        print("📴 Disconnected")

def main():
    client = LowLatencyVideoClient("192.168.0.179", 9999)  # Укажите IP сервера
    
    if client.connect():
        try:
            client.receive_video()
        except KeyboardInterrupt:
            print("\n📴 Disconnecting...")
        finally:
            client.disconnect()
    else:
        print("❌ Failed to connect")

if __name__ == "__main__":
    main()