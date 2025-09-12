#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define PORT 8080
#define BUFFER_SIZE 1024

int main() {
    printf("Start http server on the port %d\n", PORT);
    //Файловый дескриптор лдя сокета
    int server_fd;
    server_fd = socket(AF_INET, SOCK_STREAM, 0);

    //Проверка создания сокета
    if (server_fd < 0) {
        perror("Can't create socket");
        exit(EXIT_FAILURE);
    }
    //Опция для повторного использования адреса
    int opt = 1;
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        perror("Error set sockopt");
        close(server_fd);
        exit(EXIT_FAILURE);
    }
    //Настройка адреса сервера
    struct sockaddr_in address;
    socklen_t addrlen = sizeof(address);
    //Заполняем структуру адреса нулями
    memset(&address, 0, sizeof(address));
    adress.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    //Привязываем сокет к адресу и порту
    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("Binding error (bind)");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    //Прослушка входящийх соеденений
    if (listen(server_fd, 10) < 0) {
        perror("Error listenning (listen)");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Server start and listen port %d\n", PORT);
    printf("Open your browser and go to link http://localhost:%d/n", PORT);

    //Обработка соеденений
    while (1) {
        int client_socket = accept(server_fd, (struct sockaddr*)&address, (socklen_t*)&addrlen);

        if (client_socket < 0) {
            perror("Error get connect (accept)");
            continue; //Продолжаем даже если 1 соеденение фигня
        }

        printf("Get new message\n");

        //Буфер хранения HTTP запроса
        char buffer[BUFFER_SIZE] = {0};

        //Читаем запрос от клиента
        ssize_t bytes_read = read(client_socket, buffer, BUFFER_SIZE - 1);

        if (bytes_read < 0) {
    `       perror("Error read from socket");
            close(client_socket);
            continue;
        }

        //Нулевой терминал для безопасности
        buffer[bytes_read] ='\0';

        //Выводим поученный запрос для отладки
        printf("Reseived HTTP-request: \n%s\n", buffer);

        //Ищем первую строку
        char method[16], path[256], protocol[16];

        //Расчленяем первую строку
        sscanf(buffer, "%15s %255s %15s", method, path, protocol);
        printf("Method: %s, path: %s, protocol: %s\n", method, path, protocol);

        //Ответ
        char response[BUFFER_SIZE * 2];
        int response_length;

        //Чекаем какой путь запрошен и перенаправляем
        if (strcmp(path, "/") == 0) {
            const char *body = 
                "<html>"
                "<head><title>Server</title></head>"
                "<body>"
                "<h1>Wath's up</h1>"
                "<p>Building http server from scrath</p>"
                "</body>"
                "</html>";

            //Крафтим полный ответ
            response_length = snprintf(
                response, sizeof(response),
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                "Content-Length: %zu\r\n"
                "Connection: close\r\n"
                "\r\n"  
                "%s",
                strlen(body), body
            );
        } else {
            const char *body = 
                "<html>"
                "<head><title>404 - Not found</title></head>"
                "<body>"
                "<h1>404 - Peage not found</h1>"
                "<p>Server don't has this request.</p>"
                "</body>"
                "</html>";

            response_length = snprintf(
                response, sizeof(response),
                "HTTP/1.1 404 Not found\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                "Content-Length: %zu\r\n"
                "Connection: close\r\n"
                "\r\n"
                "%s",
                strlen(body), body
            );
        }

        //Отпровляем ответ клиенту
        ssize_t bytes_send = write(client_socket, response, response_length);

        if (bytes_send < 0) {
            perror("Error send answer");
        } else {
            printf("Answer send correctly (%zd bytes)\n", bytes_send);
        }
        //Обрубаем соеденение и освобождаем ресурсы
        close(client_socket);
        printf("Connection close\n\n");
    }

    //Закрываем серверный сокет
    close(server_fd);
    return 0;
}