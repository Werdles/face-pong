"""
Локальный сервер для мгновенного запуска Face Pong на телефоне через Wi-Fi.
"""
import http.server
import socket
import socketserver
import os
import sys
import qrcode

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run():
    ip = get_local_ip()
    url = f"http://{ip}:{PORT}"
    
    # Генерация QR-кода
    qr_path = os.path.join(DIRECTORY, "qr_code.png")
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(qr_path)

    print("=" * 65)
    print(" 📱 FACE PONG: СЕРВЕР ДЛЯ ТЕЛЕФОНА ЗАПУЩЕН!")
    print("=" * 65)
    print(f"\n1. Отправьте эту ссылку в Telegram (себе в 'Избранное'):")
    print(f"   >>> {url} <<<\n")
    print("2. Или наведите камеру телефона на QR-код ниже:\n")
    try:
        qr.print_ascii(invert=True)
    except Exception:
        pass
    print(f"\n3. QR-код также сохранён как картинка:")
    print(f"   {qr_path}\n")
    print("=" * 65)
    print("КАК УСТАНОВИТЬ НА РАБОЧИЙ СТОЛ ТЕЛЕФОНА:")
    print(" - На Android (Chrome/Telegram):")
    print("   Нажмите 'Добавить на главный экран' во всплывающем меню.")
    print(" - На iPhone (Safari):")
    print("   Нажмите кнопку 'Поделиться' -> 'На экран Домой'.")
    print("После этого на рабочем столе появится иконка с лицом,")
    print("а игра будет запускаться во весь экран как настоящее приложение!")
    print("=" * 65)
    print("Для остановки сервера нажмите Ctrl+C\n")

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nСервер остановлен.")

if __name__ == "__main__":
    run()
