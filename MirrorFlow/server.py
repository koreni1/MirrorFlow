import socket
import threading
import zlib  # Встроен в Python, не требует установки
import numpy as np
from mss import mss
import struct

class LowLatencyVideoServer:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.clients = []
        self.running = False
        
    def start(self):
        self.running = True
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        print(f"🚀 Server started on {self.host}:{self.port}")
        
        # Запускаем поток для захвата экрана
        capture_thread = threading.Thread(target=self.capture_and_send)
        capture_thread.daemon = True
        capture_thread.start()
        
        while self.running:
            try:
                client_socket, addr = server_socket.accept()
                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                print(f"📱 New connection from {addr}")
                self.clients.append(client_socket)
            except:
                break
        
        server_socket.close()
    
    def capture_and_send(self):
        """Захват экрана и отправка клиентам"""
        with mss() as sct:
            monitor = sct.monitors[1]  # Основной монитор
            
            while self.running:
                try:
                    # Захват экрана
                    screenshot = sct.grab(monitor)
                    
                    # Конвертация в numpy array
                    frame = np.array(screenshot)
                    
                    # Конвертация BGRA to RGB
                    frame = frame[:, :, :3]  # Убираем alpha канал
                    
                    # Компрессия (zlib встроен в Python)
                    compressed = zlib.compress(frame.tobytes(), level=1)
                    
                    # Отправка всем клиентам
                    for client in self.clients[:]:
                        try:
                            # Отправляем размер данных
                            size = struct.pack('!I', len(compressed))
                            client.sendall(size)
                            # Отправляем данные
                            client.sendall(compressed)
                        except:
                            self.clients.remove(client)
                            print("❌ Client disconnected")
                
                except Exception as e:
                    print(f"Capture error: {e}")
                    continue
    
    def stop(self):
        self.running = False

def main():
    server = LowLatencyVideoServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n🛑 Server stopping...")
        server.stop()

if __name__ == "__main__":
    main()